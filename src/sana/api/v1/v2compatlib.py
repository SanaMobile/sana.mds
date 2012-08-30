""" Utilities for transforming from the 1.x to other versions.

:Authors: Sana dev team
:Version: 1.1
"""
import logging
from django.views.generic import RedirectView
from django.views.generic.simple import redirect_to
from xml.etree import ElementTree
from xml.etree.ElementTree import parse

_deprecated = ('patientEnrolled',
              "patientId",
              "patientGender",
              'patientFirstName',
              'patientLastName',
              'patientBirthdateDay',
              'patientBirthdateMonth',
              'patientBirthdateYear',
              "patientIdNew",
              "patientGenderNew",
              'patientFirstNameNew',
              'patientLastNameNew',
              'patientBirthdateDayNew',
              'patientBirthdateMonthNew',
              'patientBirthdateYearNew',)
""" Deprecated terms not used within observations """


LCOMPLEX_TYPES = { 'PICTURE': 'image/jpeg',
                   'SOUND': 'audio/3gpp',
                   'VIDEO': 'video/3gpp',
                   'BINARYFILE': 'application/octet-stream'}

def redirect_to_v1(request, url, query_string=True, **kwargs):
    return redirect_to(request, url, query_string=query_string, **kwargs)

class V1RedirectView(RedirectView):
    query_string = True
    

def strip_deprecated_observations(observations):
    """ Removes old bio glomming in the observation dict 
        Parameters:
        observations
            A dictionary of observations.
    """
    _obs = {}
    #_obs = dict([(lambda x: (k,v) for k not in deprecated)(observations)])
    for k,v in observations.items():
        if k not in _deprecated:
            _obs[k] = v 
    return _obs

def element2obs(obs, allow_null=False):    
    """ Remaps the old format to new api Observation model for a single
        observation. Returns a dictionary, not an observation instance.
    """
    # Should only be one
    _obs = {}
    #For now we require non-empty strings
    if obs['answer']:
        _obs['value'] = obs['answer']
    else:        
        return {}
    node = obs.keys()[0]
    _obs['node'] = node
    _obs['concept'] = obs['concept']
    return _obs


def elements2obs(observations, allow_null=False):
    """ Remaps the old format to new api Observation model. Returns only the 
        text dictionary, not the actual observations.
    """
    _obs_set = {}
    for k,v in observations.items():
        _obs = {}
        #For now we require non-empty strings
        if v['answer']:
            _obs['value'] = v['answer']
        else:
            continue
        _obs['node'] = k
        _obs['concept'] = v['concept']
        logging.debug('Obs: %s' % _obs)
        _obs_set[k] = _obs
    return _obs_set

# TODO
def bchunk2bpacket(form):
    """ Converts the old binary chunk packet form into the v2 api
    """
    encounter = form.cleaned_data['procedure_guid']
    node = form.cleaned_data['element_id']
    subnode = form.cleaned_data['binary_guid']
    node = '%s-%s'% (node, subnode)
    type = form.cleaned_data['element_type']
    size = form.cleaned_data['file_size']
    offset = form.cleaned_data['byte_start']
    byte_end = form.cleaned_data['byte_end']
    return {}

class LProcedureParsable:
    """ A new parsed legacy procedure backed by an ElementTree.
        The default behavior of the constructor is to use the 
        text parameter as the xml if both text and xml are not None 
        
            Parameters
                text
                    An xml string
                path
                    The path to a file containing the xml to parse
        """
    def __init__(self, text=None, path=None ):
        self.root = None
        self._parse(text=text, path=path)
        
    def _parse(self, text=None, path=None):
        if text:
            self.root = ElementTree.XML(text)
        elif path: 
            self.root = parse(path).getroot()
        
    def __call__(self,text=None, path=None):
        self._parse(text=text, path=path)
    
    @property
    def concepts(self):
        def _map(x):
            mime = LCOMPLEX_TYPES.get(x.attrib['type'], 'text/plain')
            return { 'name' : x.attrib['concept'], 
                     'description' : x.attrib['question'],
                     'is_complex' : (mime != 'text/plain'),
                     'data_type' : mime }
        return list(_map(x) for x in self.root.findall('Page/Element'))
    
    @property
    def pages(self):
        return list(x for x in self.root.findall('Page'))
    
    @property
    def elements(self):
        return list(x.attrib for x in self.root.findall('Page/Element'))
        
    def to_python(self):
        ''' Converts the parsed object to a dict '''
        _p = {}
        self._rdict(_p, self.root)
        return _p
    
    def _rdict(self, pdict, node, indent=0):
        """ Recursive helper method for building the python object """
        # append all of the children as 'tag': dict([*node.attrs, dict(children)
        _current = node.attrib
        for n in list(node):
            _a = {}
            self._append(_current, n, indent+4)
            if n.tag in _current:
                list(_current[n.tag]).append(_a)
            else:
                _current[n.tag] = _a
        pdict[node.tag] = _current
    
lpp = LProcedureParsable

if __name__ == '__main__':
    """ Run this as 
            python legacy_utils.py procedure $FILE
        to print a procedure to stdout
    """
    import sys
    if sys.argv[1] == 'p':
        _ptext = sys.argv[3]
        _pr = lpp(path=_ptext)
        if sys.argv[2] == 'p':
            print ' '*4,_pr.root.attrib
        elif sys.argv[2] == 'e':
            for e in _pr.elements:
                print ' '*4, e
        elif sys.argv[2] == 'c':
            for c in _pr.concepts:
                print c
    
