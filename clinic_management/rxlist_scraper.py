"""
RxList Drug Scraper (Fixed)
============================
Cào dữ liệu thuốc từ https://www.rxlist.com/drugs/alpha_a.htm (từ A đến Z)
Các trường: name, generic_name, category, unit, description, side_effect

Cấu trúc trang đã được inspect và verify:
  - Trang index : các link thuốc nằm trong <ul> > <li> > <a href="...-drug.htm">
  - Trang detail: Drug Summary section chứa đủ generic_name, category, unit, desc, side_effect

Requirements:
    pip install selenium webdriver-manager

Usage:
    python rxlist_scraper.py                        # cào toàn bộ A-Z
    python rxlist_scraper.py --letters a b c        # chỉ cào a, b, c
    python rxlist_scraper.py --output result.csv --delay 2.0
    python rxlist_scraper.py --no-headless --letters a   # debug có UI
"""

import argparse
import csv
import logging
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WDM = True
except ImportError:
    USE_WDM = False

# ──────────────────────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("rxlist_scraper.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────
BASE_INDEX_URL = "https://www.rxlist.com/drugs/alpha_{letter}.htm"
ALPHABET       = list("abcdefghijklmnopqrstuvwxyz")
DEFAULT_DELAY  = 1.5     # giây chờ giữa mỗi trang chi tiết
DEFAULT_OUTPUT = "drugs.csv"
WAIT_TIMEOUT   = 15

FIELDNAMES = ["name", "generic_name", "category", "unit",
              "description", "side_effect", "source_url"]


# ──────────────────────────────────────────────────────────────
# DATA MODEL
# ──────────────────────────────────────────────────────────────
@dataclass
class Drug:
    name:         str = ""
    generic_name: str = ""
    category:     str = ""
    unit:         str = ""
    description:  str = ""
    side_effect:  str = ""
    source_url:   str = ""


# ──────────────────────────────────────────────────────────────
# DRIVER
# ──────────────────────────────────────────────────────────────
def build_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if USE_WDM:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
    else:
        driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"},
    )
    return driver


# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────
def wait_for(driver, css_selector: str, timeout: int = WAIT_TIMEOUT) -> bool:
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        return True
    except TimeoutException:
        return False


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_section_text(driver, heading_keyword: str, max_paras: int = 5) -> str:
    """
    Tìm thẻ h4 chứa heading_keyword, rồi gộp text các thẻ ngay sau
    cho đến khi gặp heading kế tiếp.
    """
    try:
        headings = driver.find_elements(By.CSS_SELECTOR, "h4")
        for h in headings:
            if heading_keyword.lower() in h.text.lower():
                parts  = []
                count  = 0
                sibling = driver.execute_script(
                    "return arguments[0].nextElementSibling;", h
                )
                while sibling and count < max_paras:
                    tag = sibling.tag_name.lower()
                    if tag in ("h2", "h3", "h4"):
                        break
                    t = sibling.text.strip()
                    if t:
                        parts.append(t)
                    sibling = driver.execute_script(
                        "return arguments[0].nextElementSibling;", sibling
                    )
                    count += 1
                return clean(" ".join(parts))
    except Exception:
        pass
    return ""


# ──────────────────────────────────────────────────────────────
# STEP 1 – LẤY DANH SÁCH LINK THUỐC TỪ TRANG INDEX
# ──────────────────────────────────────────────────────────────
def get_drug_links(driver, letter: str) -> list:
    """
    Trang index có dạng:
        <li><a href="https://www.rxlist.com/abilify-drug.htm">Abilify (Aripiprazole)</a></li>

    => Selector: tất cả <a> có href kết thúc bằng '-drug.htm'
    """
    url = BASE_INDEX_URL.format(letter=letter.lower())
    log.info(f"[{letter.upper()}] Tải trang index: {url}")

    try:
        driver.get(url)
    except WebDriverException as e:
        log.error(f"[{letter.upper()}] Không tải được: {e}")
        return []

    # Chờ body sẵn sàng
    wait_for(driver, "body", timeout=20)
    time.sleep(1.5)

    links = []
    seen  = set()
    try:
        anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        for a in anchors:
            href = (a.get_attribute("href") or "").strip()
            name = a.text.strip()

            # Chỉ giữ link dạng: https://www.rxlist.com/xxx-drug.htm
            if (
                href
                and name
                and href.endswith("-drug.htm")
                and "rxlist.com" in href
                and href not in seen
            ):
                seen.add(href)
                links.append({"name": name, "url": href})

    except Exception as e:
        log.error(f"[{letter.upper()}] Lỗi khi quét anchor: {e}")

    log.info(f"[{letter.upper()}] => Tìm thấy {len(links)} thuốc.")
    return links


# ──────────────────────────────────────────────────────────────
# STEP 2 – CÀO CHI TIẾT TỪNG THUỐC
# ──────────────────────────────────────────────────────────────
def parse_drug_detail(driver, drug_info: dict) -> Drug:
    """
    Cấu trúc trang chi tiết (phần Drug Summary):

      # Abilify
      Generic Name: aripiprazole
      Brand Name: Abilify
      Drug Class: Antipsychotics, Second Generation | Antimanic Agents

      #### What Is Abilify?       -> description
      #### What Are Side Effects? -> side_effect
      #### Dosage for Abilify     -> unit (dạng bào chế)
    """
    url  = drug_info["url"]
    drug = Drug(name=drug_info["name"], source_url=url)

    try:
        driver.get(url)
    except WebDriverException as e:
        log.error(f"  Lỗi tải {url}: {e}")
        return drug

    if not wait_for(driver, "body", timeout=15):
        log.warning(f"  Timeout: {url}")
        return drug

    time.sleep(0.5)

    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text
    except Exception:
        body_text = ""

    # ── generic_name ──────────────────────────────────────────
    m = re.search(r"Generic Name[s]?:\s*([^\n]+)", body_text, re.IGNORECASE)
    if m:
        drug.generic_name = clean(m.group(1))

    # ── category ──────────────────────────────────────────────
    m = re.search(r"Drug Class(?:es)?:\s*([^\n]+)", body_text, re.IGNORECASE)
    if m:
        drug.category = clean(m.group(1))

    # ── description (What Is ...) ─────────────────────────────
    drug.description = extract_section_text(driver, "What Is", max_paras=3)
    if not drug.description:
        # Fallback: đoạn văn dài đầu tiên trong trang
        try:
            for p in driver.find_elements(By.CSS_SELECTOR, "p"):
                t = p.text.strip()
                if len(t) > 100:
                    drug.description = clean(t)
                    break
        except Exception:
            pass

    # ── side_effect (What Are Side Effects ...) ───────────────
    drug.side_effect = extract_section_text(driver, "Side Effect", max_paras=6)

    # ── unit / dosage form (Dosage for ...) ───────────────────
    dosage_text = extract_section_text(driver, "Dosage", max_paras=2)
    if dosage_text:
        # "Abilify is available in tablet, orally disintegrating tablets, ..."
        m = re.search(
            r"available (?:in|as)\s+(.+?)(?:\.|Dosage|$)",
            dosage_text, re.IGNORECASE
        )
        drug.unit = clean(m.group(1)) if m else clean(dosage_text[:200])

    log.debug(
        f"  ✓ {drug.name[:40]:40s} | "
        f"generic={drug.generic_name[:20]} | cat={drug.category[:25]}"
    )
    return drug


# ──────────────────────────────────────────────────────────────
# CSV
# ──────────────────────────────────────────────────────────────
def init_csv(path: Path) -> None:
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()
        log.info(f"Tạo file CSV mới: {path}")
    else:
        log.info(f"Ghi thêm vào file hiện có: {path}")


def append_csv(path: Path, drug: Drug) -> None:
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow(asdict(drug))


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="RxList Drug Scraper")
    parser.add_argument("--letters", nargs="+", default=ALPHABET,
                        help="Chữ cái cần cào, vd: a b c (mặc định: a-z)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help=f"File CSV đầu ra (mặc định: {DEFAULT_OUTPUT})")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                        help=f"Giây chờ giữa trang chi tiết (mặc định: {DEFAULT_DELAY})")
    parser.add_argument("--headless", dest="headless",
                        action="store_true", default=True)
    parser.add_argument("--no-headless", dest="headless",
                        action="store_false",
                        help="Hiện cửa sổ Chrome (dùng để debug)")
    args = parser.parse_args()

    letters = [l.lower() for l in args.letters if l.isalpha()]
    output  = Path(args.output)

    log.info(f"Output   : {output.resolve()}")
    log.info(f"Chữ cái  : {', '.join(l.upper() for l in letters)}")
    log.info(f"Delay    : {args.delay}s | Headless: {args.headless}")

    init_csv(output)
    driver = build_driver(headless=args.headless)
    total  = 0

    try:
        for letter in letters:
            # --- Lấy danh sách link từ trang index ---
            drug_links = get_drug_links(driver, letter)
            if not drug_links:
                log.warning(f"[{letter.upper()}] Không có link nào – bỏ qua.")
                continue

            # --- Vào từng trang thuốc để cào ---
            for idx, info in enumerate(drug_links, 1):
                log.info(
                    f"[{letter.upper()}] ({idx}/{len(drug_links)}) "
                    f"Đang cào: {info['name']}"
                )
                try:
                    drug = parse_drug_detail(driver, info)
                    append_csv(output, drug)
                    total += 1
                except Exception as e:
                    log.error(f"  Lỗi: {e} — URL: {info['url']}")

                time.sleep(args.delay)

            log.info(f"[{letter.upper()}] Xong. Tổng đã lưu: {total} thuốc.")

    except KeyboardInterrupt:
        log.info("Dừng (Ctrl+C). Dữ liệu đã lưu vẫn an toàn trong CSV.")
    finally:
        driver.quit()
        log.info(f"Kết thúc. Tổng: {total} thuốc → {output.resolve()}")


if __name__ == "__main__":
    main()
