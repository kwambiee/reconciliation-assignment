from django.shortcuts import render
import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

class ReconciliationView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        source_file = request.FILES.get('source')
        target_file = request.FILES.get('target')

        if not source_file or not target_file:
            return Response({'error': 'Both source and target files are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            source_data = self.parse_csv(source_file)
            target_data = self.parse_csv(target_file)
        except Exception as e:
            return Response({'error': f'CSV parsing error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        report = self.reconcile(source_data, target_data)
        return Response(report, status=status.HTTP_200_OK)

    def parse_csv(self, file):
        decoded = file.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(decoded))
        return [self.normalize_row(row) for row in reader]

    def normalize_row(self, row):
        return {key.strip().lower(): value.strip().lower() for key, value in row.items()}

    def reconcile(self, source, target):
        source_ids = {row['id']: row for row in source}
        target_ids = {row['id']: row for row in target}

        missing_in_target = [v for k, v in source_ids.items() if k not in target_ids]
        missing_in_source = [v for k, v in target_ids.items() if k not in source_ids]
        discrepancies = []

        for key in source_ids.keys() & target_ids.keys():
            src_row = source_ids[key]
            tgt_row = target_ids[key]
            diff = {f: {'source': src_row[f], 'target': tgt_row[f]} 
                    for f in src_row if src_row[f] != tgt_row.get(f)}
            if diff:
                discrepancies.append({
                    'id': key,
                    'differences': diff
                })

        return {
            'missing_in_target': missing_in_target,
            'missing_in_source': missing_in_source,
            'discrepancies': discrepancies
        }
