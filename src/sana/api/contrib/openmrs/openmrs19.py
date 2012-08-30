""" Classes and utilities for talking to an OpenMRS server version 1.9

:Authors: Sana Dev Team
:Version: 2.0
"""
import urllib
import cookielib
import logging
import urllib2
import cjson
import time

from django.conf import settings

from sana.api.contrib import handlers
from sana.api.contrib.openmrs import openers

__all__ = ['OpenMRS']

class OpenMRS(openers.OpenMRSOpener):
    """Utility class for remote communication with OpenMRS version 1.9"""
    _create_session =  None,
    _read_credentials = "loginServlet",
    _read_subject = "moduleServlet/ws/rest/v1/patient/{uuid}"
    _create_subject = "admin/patients/newPatient.form"
    _create_encounter = "moduleServlet/sana/uploadServlet"
    _read_encounter = "moduleServlet/ws/rest/v1/encounter/{uuid}"
    _read_encounter_observations = "moduleServlet/ws/rest/v1/encounter/{uuid}/observation/?v=full", 
    
    def validate_patient(self, uuid=""):
        pass
    
    def getPatient(self,username, password, patientid):
        """ Retrieves a patient by id from OpenMRS through the Webservices.REST 
            module.

            REST module url: <host> + patient/{patientid}
        
        Parameters:
            username
                OpenMRS username
            password
                OpenMRS password
            userid
                patient identifier
           
        """
        path = self._get_path('_read_subject')
        uri = self.url + path.format(uuid=patientid)

        cookies = cookielib.CookieJar()
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, uri, username, password)
        auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(auth_handler,
                                      urllib2.HTTPCookieProcessor(cookies),
                                      handlers.MultipartPostHandler)
        urllib2.install_opener(opener)
        rest = urllib2.urlopen(uri)
        return rest.read()
    
    def getAllPatients(self,username, password):
        """Retrieves all patients from OpenMRS through the REST module.

        OpenMRS url: <host> + moduleServlet/restmodule/api/allPatients/
        
        Parameters:
            username
                OpenMRS username
            password
                OpenMRS password
            userid
                patient identifier
           
        """
        uri = self.url+'moduleServlet/restmodule/api/allPatients/'
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, uri, username, password)
        auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(auth_handler,
                                      urllib2.HTTPCookieProcessor(self.cookies),
                                      handlers.MultipartPostHandler)
        urllib2.install_opener(opener)
        rest = urllib2.urlopen(uri)
        return rest.read()
    
    def create_patient(self, patient_id, first_name, last_name, gender, 
                       birthdate):
        """Sends a post request to OpenMRS patient service to create patient.
                
        OpenMRS url: <host> + admin/patients/newPatient.form
           
        OpenMRS Form Fields: ::
        
            Parameters    OpenMRS form field    Note
            first_name    name.givenName        N/A
            last_name     name.familyName       N/A
            patient_id    identifier            N/A
            gender        gender                M or F
            birthdate     birthdate             single digits must be padded            
            N/A           identifierType        use "2"
            N/A           location              use "1"
        
        Parameters:
            patient_id
                client generated identifier
            first_name
                patient given name
            last_name
                patient family name
            gender
                M or F
            birthdate
                patient birth date formatted as mm/dd/yyyy
        """
        try:
            if len(self.cookies) == 0:
                self._login()
            parameters = {"name.givenName": first_name,
                          "name.familyName": last_name,
                          "identifier": patient_id,
                          "identifierType": 2,
                          "location": 1,
                          'gender': gender,
                          'birthdate': birthdate,}
            #parameters = urllib.urlencode(parameters)
            url = "%sadmin/patients/newPatient.form" % self.url
            logging.info("Creating new patient %s" % patient_id)
            self.opener.open(url, parameters)
        except Exception, e:
                logging.info("Exception trying to create patient: %s" % str(e))

    def _login(self):
        loginParams = urllib.urlencode(
            {"uname": self.username,
             "pw": self.password,
             "redirect": "/openmrs",
             "refererURL": self.url+"index.htm"
             })
        try:
            self.opener.open("%sloginServlet" % self.url, loginParams)
            logging.debug("Success: Validating with OpenMRS loginServlet")
            result = True
        except Exception, e:
            logging.debug("Error logging into OpenMRS: %s" % e)
            result = False
        return result
    
    def upload_procedure(self, patient_id, phone_id,
                         procedure_title, saved_procedure_id,
                         responses, files):
        """Posts an encounter to the OPenMRS encounter service through the Sana
        module
        
        OpenMRS url: <host> + moduleServlet/moca/uploadServlet
        
        OpenMRS Form Fields: ::
        
            Parameter             OpenMRS form field    Note
            phone_id              phoneId
                                  procedureDate         mm/dd/yyyy
            patient_id            patientId
            procedure_title       procedureTitle
            saved_procedure_id    caseIdentifier
            responses             questions
            
        Note: Above parameters are then encoded and posted to OpenMRS as the
        'description' field value.
            
        Binaries are attached as one parameter per binary with field name
        given as 'medImageFile-<element-id>-<index> where index correlates 
        to the position in the csv 'answer' attribute of the particular 
        procedure element
        
        Parameters:
            phone_id
                client telephone number.     
            patient_id   
                The patient identifier.
            procedure_title
                The procedure tirle.
            saved_procedure_id
                Saved procedure id.
            responses
                Encounter text data as JSON encoded text.
        """
        hasPermissions = False 
        result = False
        message = ""
        encounter = None
        response = None
        try:
            if len(self.cookies) == 0:
                self._login()
    
            logging.debug("Validating permissions to manage sana queue")

            url = "%smoduleServlet/sana/permissionsServlet" % self.url
            response = self.opener.open(url).read()
            logging.debug("Got result %s" % response)
            resp_msg = cjson.decode(response,True)
            message = resp_msg['message']
            hasPermissions = True if resp_msg['status'] == 'OK' else False
            if not hasPermissions:
                return result, message
            
            logging.debug("Uploading procedure")
            # NOTE: Check version format in settings matches OpenMRS version
            description = {'phoneId': str(phone_id),
                           'procedureDate': time.strftime(
                                                    settings.OPENMRS_DATE_FMT),
                           'patientId': str(patient_id),
                           'procedureTitle': str(procedure_title),
                           'caseIdentifier': str(saved_procedure_id),
                           'questions': responses}
            
            description = cjson.encode(description)
            post = {'description': str(description)}
            logging.debug("Encoded parameters, checking files.")
            # Attach a file 
            for elt in responses:
                etype = elt.get('type', None)
                eid = elt.get('id', None)
                if eid in files:
                    logging.info("Checking for files associated with %s" % eid)
                    for i,path in enumerate(files[eid]):
                        logging.info('medImageFile-%s-%d -> %s' 
                                     % (eid, i, path))
                        post['medImageFile-%s-%d' % (eid, i)] = open(path, "rb")

            url = "%smoduleServlet/moca/uploadServlet" % self.url
            logging.debug("About to post to " + url)
            response = self.opener.open(url, post).read()
            logging.debug("Got result %s" % response)
                
            resp_msg = cjson.decode(response,True)
            message = resp_msg.get('message', '')
            result = True if resp_msg['status'] == 'OK' else False
            encounter = resp_msg.get('encounter', None)
            logging.debug("Done with upload")
            
        except Exception as e:
            logging.error("Exception in uploading procedure: %s" 
                          % saved_procedure_id)
            raise e
        return result, message, encounter
