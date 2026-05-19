import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from app.models import Drug


class Command(BaseCommand):

    help = "Import drugs from CSV"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        drugs = []

        with open(
            "drugs.csv",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                drugs.append(
                    Drug(
                        name=row["name"].strip(),

                        generic_name=row.get(
                            "generic_name",
                            ""
                        ).strip(),

                        category=row.get(
                            "category",
                            "other"
                        ).strip(),

                        unit=row.get(
                            "unit",
                            "viên"
                        ).strip(),

                        description=row.get(
                            "description",
                            ""
                        ).strip(),

                        side_effects=row.get(
                            "side_effect",
                            ""
                        ).strip(),

                        is_active=True
                    )
                )

        Drug.objects.bulk_create(
            drugs,
            batch_size=1000
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(drugs)} drugs successfully"
            )
        )