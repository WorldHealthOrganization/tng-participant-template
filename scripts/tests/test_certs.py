'''This is a collection of tests that target certificate files'''

from valid_pem import test_valid_pem
from signature_algorithm import test_signature_algorithm
from key_length import test_key_length
from subject_format import test_subject_format
from country_flag import test_country_flag
# from oversea_territory import test_oversea_territory_ou # TODO: implement
from validity import test_validity
from validity_range import test_validity_range
# from explicit_parameters import test_explicit_parameter # TODO: implement
from extended_key_usage import test_extended_key_usages
from key_usage import test_key_usages
from basic_constraints import test_basic_constraints
from tls_pem_without_chain import test_tls_pem_without_chain
from chain_check import test_if_tls_resolves