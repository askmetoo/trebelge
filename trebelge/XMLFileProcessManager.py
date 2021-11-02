from trebelge.XMLFileTypeState import XMLFileTypeContext
from trebelge.XMLFileCoR import AbstractXMLFileHandler
from trebelge.XMLFileCoR.InvoiceHandler import InvoiceHandler


class XMLFileProcessManager:
    # initiate Context of State pattern for FileType
    cXMLFileTypeContext = XMLFileTypeContext()
    # initiate CoR pattern for xmlFile
    hXMLFileTypeHandler: AbstractXMLFileHandler = InvoiceHandler()

    def __init__(self, file_path: str):
        self.hXMLFileTypeHandler.handle_xml_file_type(file_path, self.cXMLFileTypeContext)
