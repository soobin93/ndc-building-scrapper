from realestate import get_properties as get_re_properties
from domain import get_properties as get_domain_properties
from exporter import save_to_file

properties = []

properties += get_re_properties()
properties += get_domain_properties()

save_to_file(properties)
