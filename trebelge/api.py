import frappe
import xml.etree.ElementTree as ET

from xml.etree.ElementTree import XMLParser
from trebelge.EbelgeUsers import EbelgeUsers
from trebelge.incomingEfaturaReader import incomingEfaturaReader


@frappe.whitelist()
def check_all_ebelge_parties():
    ebelge_users = get_ebelge_users()
    for party_type in ["Customer", "Supplier"]:
        for party in frappe.get_all(party_type, filters={"tax_id": ["not in", None], "disabled": 0},
                                    fields={"name", "tax_id", "is_efatura_user", "is_eirsaliye_user"}):
            if party["tax_id"] in ebelge_users:
                if ebelge_users[party["tax_id"]]["is_efatura_user"]:
                    if party["is_efatura_user"] != 1:
                        doc = frappe.get_doc(party_type, party.name)
                        doc.db_set("is_efatura_user", 1)
                else:
                    if party["is_efatura_user"] == 1:
                        doc = frappe.get_doc(party_type, party.name)
                        doc.db_set("is_efatura_user", 0)
                if ebelge_users[party["tax_id"]]["is_eirsaliye_user"]:
                    if party["is_eirsaliye_user"] != 1:
                        doc = frappe.get_doc(party_type, party.name)
                        doc.db_set("is_eirsaliye_user", 1)
                else:
                    if party["is_eirsaliye_user"] == 1:
                        doc = frappe.get_doc(party_type, party.name)
                        doc.db_set("is_eirsaliye_user", 0)
            else:
                if party["is_efatura_user"] == 1:
                    doc = frappe.get_doc(party_type, party.name)
                    doc.db_set("is_efatura_user", 0)
                if party["is_eirsaliye_user"] == 1:
                    doc = frappe.get_doc(party_type, party.name)
                    doc.db_set("is_eirsaliye_user", 0)
    return frappe.utils.nowdate()


def get_ebelge_users():
    parser = XMLParser(target=EbelgeUsers())
    parser.feed(
        frappe.read_file(frappe.get_site_path("private", "files", "KullaniciListesiXml", "newUserPkList.xml")))
    return parser.close()


def read_ebelge_file():
    filename = '/home/tufankaynak/bench/sites/trgibebelgedev/private/files/13D2021000002726.xml'
    namespaces = read_all_namespaces(filename)
    if ET.parse(filename).getroot().tag == '{' + namespaces.get('') + '}Invoice':
        parser = XMLParser(target=incomingEfaturaReader(namespaces))
        parser.feed(frappe.read_file(filename))
        return parser.close()


def read_all_namespaces(filename):
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    return namespaces
