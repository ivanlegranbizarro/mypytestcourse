import json
from py import path
import pytest
from unittest import TestCase
from django.test import Client
from django.urls import reverse
from companies.models import Company


@pytest.mark.django_db
class BasicCompanyApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse('companies-list')

    def tearDown(self) -> None:
        pass


class TestGetCompanies(BasicCompanyApiTestCase):

    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        test_company = Company.objects.create(name='Amazon')
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get('name'), test_company.name)
        self.assertEqual(response_content.get('status'), 'Hiring')
        self.assertEqual(response_content.get('application_link'), '')
        self.assertEqual(response_content.get('notes'), '')

        test_company.delete()


class TestPostCompanies(BasicCompanyApiTestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(
            response.content
        ),
            {"name": ["This field is required."]}
        )

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name='Apple')
        response = self.client.post(path=self.companies_url,
                                    data={
                                        "name": "Apple",
                                    })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(
            response.content
        ),
            {"name": ["company with this name already exists."]}
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(path=self.companies_url,
                                    data={
                                        "name": "Test Company 1",
                                    })
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get('name'), 'Test Company 1')
        self.assertEqual(response_content.get('status'), 'Hiring')
        self.assertEqual(response_content.get('application_link'), '')
        self.assertEqual(response_content.get('notes'), '')

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(path=self.companies_url,
                                    data={
                                        "name": "Test Company 1",
                                        "status": "Layoffs"
                                    })
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get('name'), 'Test Company 1')
        self.assertEqual(response_content.get('status'), 'Layoffs')


@pytest.mark.xfail
def test_should_be_ok_if_fails(self) -> None:
    self.assertEqual(1, 2)


@pytest.mark.skip
def test_should_be_skipped(self) -> None:
    self.assertEqual(1, 2)


def raise_covid19_exception() -> None:
    raise ValueError('Coronavirus Exception')


def test_raise_covid_19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert 'Coronavirus Exception' == str(e.value)
