import argparse
import json
import sys, os

import django
from django.db import IntegrityError

sys.path.append('./')
os.environ['DJANGO_SETTINGS_MODULE'] = 'alkaf_administration.settings'
django.setup()

from transaction.models import City, Product, Courier, Marketplace, Customer


def read_csv_file(path):
    with open(path, 'r') as f_in:
        return list(map(lambda x: x.strip().split(','), f_in.readlines()))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--product_data_file_path',
        type=str,
    )
    argparser.add_argument(
        '--city_data_file_path',
        type=str,
    )
    argparser.add_argument(
        '--courier_data_file_path',
        type=str,
    )
    argparser.add_argument(
        '--marketplace_data_file_path',
        type=str,
    )
    argparser.add_argument(
        '--customer_data_file_path',
        type=str,
    )
    args = argparser.parse_args()

    if args.product_data_file_path:
        lines = read_csv_file(args.product_data_file_path)
        for line in lines:
            if 'HD' in line[0]:
                code = line[0]
                name = line[0].split('-')[0]
                color = line[1]
                size = line[2]
                try:
                    Product.objects.get_or_create(code=code, name=name, color=color, size=size)
                except IntegrityError as e:
                    print(e)
                    print(line)

    if args.city_data_file_path:
        lines = read_csv_file(args.city_data_file_path)
        for line in lines:
            city_name = line[2]
            try:
                City.objects.get_or_create(name=city_name.upper())
            except IntegrityError as e:
                print(e)
                print(line)

    if args.courier_data_file_path:
        lines = read_csv_file(args.courier_data_file_path)
        for line in lines:
            name = line[0]
            type = line[1]
            short_name = line[2] if line[2] else None
            try:
                Courier.objects.get_or_create(name=name, type=type, short_name=short_name)
            except IntegrityError as e:
                print(e)
                print(line)

    if args.marketplace_data_file_path:
        lines = read_csv_file(args.marketplace_data_file_path)
        for line in lines:
            name = line[0]
            short_name = line[1]
            try:
                Marketplace.objects.get_or_create(name=name, short_name=short_name)
            except IntegrityError as e:
                print(e)
                print(line)

    if args.customer_data_file_path:
        lines = read_csv_file(args.customer_data_file_path)
        for line in lines:
            name = line[0]
            username = line[1] if line[1] else None
            try:
                Customer.objects.get_or_create(name=name, username=username)
            except IntegrityError as e:
                print(e)
                print(line)
