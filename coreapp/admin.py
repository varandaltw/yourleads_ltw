import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Report
import xlsxwriter  # Install using pip install xlsxwriter
from io import BytesIO
from reportlab.pdfgen import canvas


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Report model, with export functionality.
    """

    # Fields to display in admin
    list_display = ('id', 'name', 'email', 'phone', 'age', 'creation_date')

    # Actions for exporting data
    actions = ['export_to_csv', 'export_to_excel', 'export_to_pdf']

    def export_to_csv(self, request, queryset):
        """
        Exports selected reports to a CSV file.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reports.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Age', 'Creation Date'])

        for report in queryset:
            writer.writerow([report.id, report.name, report.email, report.phone, report.age, report.creation_date])

        return response

    export_to_csv.short_description = "Export to CSV"

    def export_to_excel(self, request, queryset):
        """
        Exports selected reports to an Excel file.
        """
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        headers = ['ID', 'Name', 'Email', 'Phone', 'Age', 'Creation Date']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        for row_num, report in enumerate(queryset, start=1):
            worksheet.write(row_num, 0, report.id)
            worksheet.write(row_num, 1, report.name)
            worksheet.write(row_num, 2, report.email)
            worksheet.write(row_num, 3, report.phone)
            worksheet.write(row_num, 4, report.age)
            worksheet.write(row_num, 5, str(report.creation_date))

        workbook.close()
        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="reports.xlsx"'

        return response

    export_to_excel.short_description = "Export to Excel"

    def export_to_pdf(self, request, queryset):
        """
        Exports selected reports to a PDF file.
        """
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reports.pdf"'

        p = canvas.Canvas(response)
        y = 800
        p.drawString(100, y, "Reports:")
        y -= 20

        for report in queryset:
            p.drawString(100, y, f"ID: {report.id}, Name: {report.name}, Email: {report.email}, Phone: {report.phone}")
            y -= 20

        p.showPage()
        p.save()
        return response

    export_to_pdf.short_description = "Export to PDF"
