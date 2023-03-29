#! /usr/bin/python3
"""
Create on 2020
@autor Pedro J. Bartolomey Nadal
Esta libreria es la que maneja los ini
"""
# import necessary modules
import os
import sys
import configparser
from configparser import SafeConfigParser
from os import path


# Routine: Read variables from ini file
def readini(inifile,seccion,variable):
#    print (inifile)
#    print (seccion)
#    print (variable)
    message = 0
    cparser = SafeConfigParser()
    cparser.read(inifile)
    if cparser.has_section(seccion):
        if cparser.has_option(seccion, variable):
            variable = cparser.get( seccion, variable)
        else:
            message = ('Error ' + str(seccion) + '\t' + str(variable))
    else:
        message = ('Error ' + str(inifile) + '\t' + str(seccion) + '\t' + str(variable))
    return(variable,message)


# Routine: Read DMM flags from ini file.
def readini_dmmflags(inifile):
#    print (inifile)
    dmm_flags = {'acdc':'', 'measure':'', 'range':''}
    cparser = SafeConfigParser()
    cparser.read(inifile)
    ok = 0
    message = ' '
    if cparser.has_option('DMMconfig', 'acdc'):
        if cparser.get('DMMconfig', 'acdc') == 'DC':
            dmm_flags.update({'acdc':'DC'})
        elif cparser.get('DMMconfig', 'acdc') == 'AC':
            dmm_flags.update({'acdc':'AC'})
        elif cparser.get('DMMconfig', 'acdc') == '--':
            dmm_flags.update({'acdc':'--'})
        else:
            ok = 1
            message = "Wrong DMMconfig acdc." 
    else:
        ok = 1
        message = "DMMconfig acdc don't exist." 
    if cparser.has_option('DMMconfig', 'measure'):
        if cparser.get('DMMconfig', 'measure') == 'V':
            dmm_flags.update({'measure':'V'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == 'mV':
            dmm_flags.update({'measure':'mV'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == 'A':
            dmm_flags.update({'measure':'A'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == 'mA':
            dmm_flags.update({'measure':'mA'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == 'µA':
            dmm_flags.update({'measure':'µA'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == '%':
            dmm_flags.update({'measure':'%'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == 'Hz':
            dmm_flags.update({'measure':'Hz'})
            dmm_flags.update({'range':'Autorange'})
        elif cparser.get('DMMconfig', 'measure') == 'MΩ':
            dmm_flags.update({'measure':'MΩ'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == 'kΩ':
            dmm_flags.update({'measure':'kΩ'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == 'Ω':
            dmm_flags.update({'measure':'Ω'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == 'nF':
            dmm_flags.update({'measure':'nF'})
            dmm_flags.update({'range':'Autorange'})
        elif cparser.get('DMMconfig', 'measure') == 'µF':
            dmm_flags.update({'measure':'µF'})
            dmm_flags.update({'range':'Autorange'})
        elif cparser.get('DMMconfig', 'measure') == '°C':
            dmm_flags.update({'measure':'°C'})
            dmm_flags.update({'range':'Manual'})
        elif cparser.get('DMMconfig', 'measure') == '°F':
            dmm_flags.update({'measure':'°F'})
            dmm_flags.update({'range':'Manual'})
        else:
            ok = 1
            message = "Wrong DMMconfig measure." 
    else:
        ok = 1
        message = "DMMconfig measure don't exist." 
    if (ok == 0):
        return (dmm_flags,message)
    elif (ok == 1):
        return (1,message)


# Routine: Read DMM test Point/s from ini file.
def readini_point(inifile):
#    print (inifile)
    checkdata = []
    cparser = SafeConfigParser()
    cparser.read(inifile)
    ok = 0
    message = 0
    i = 1
    while cparser.has_section('Point-' + str(i)):
        if ((cparser.has_option('Point-' + str(i), 'Data')) and (cparser.has_option('Point-' + str(i), 'Tol'))):
            if cparser.has_option('Point-' + str(i), 'Name'):
                name = cparser.get('Point-' + str(i), 'Name')
            else:
                name = ' '
            if cparser.has_option('Point-' + str(i), 'Rel'):
                rel = int(cparser.get('Point-' + str(i), 'Rel')[-1])
            else:
                rel = 0
            try:
                data = float(cparser.get('Point-' + str(i), 'Data'))
            except:
                message = 'Fail in Point-' + i + 'data not float: ' + cparser.get('Point-' + str(i), 'Data')
                ok = 2
                break
            try:
                tol = float(cparser.get('Point-' + str(i), 'Tol'))
            except:
                message = 'Fail in Point-' + str(i) + 'Tolerance not float: ' + cparser.get('Point-' + str(i), 'Tol')
                ok = 2
                break
            if (rel != 0) and not(cparser.has_option('Point-' + str(rel), 'Data')) and (rel >= i):
                message = 'Fail in Point-' + str(i) + " rel don't exist: " + str(rel)
                ok = 2
                break
            if (rel != 0) and (rel >= i):
                message = 'Fail in Point-' + str(i) + ' relative Point-'  + str(rel) + ' will be read after. '
                ok = 2
                break
            checkdata.append([i,name,data,tol,rel])
        else:
            ok = 1
            message = 'Fail in Point-' + str(i) + '\n'                     \
                        + ' has Data: '                                     \
                        + str(cparser.has_option('Point-' + str(i), 'Data'))\
                        + '\n has Tol: '                               \
                        + str(cparser.has_option('Point-' + str(i), 'Tol'))
            break
        i = i + 1
    if (ok == 0):
        return (checkdata,message)
    elif (ok == 1):
        return (1,message)
    else:
        return (0,message)


# Routine: Write variables in ini file.
def writeini(inifile,seccion,variable,valor):
    cparser = SafeConfigParser()
    cparser.read(inifile)
    if cparser.has_option(seccion, variable):
        cparser.set( seccion, variable, valor)
        with open(inifile, 'w') as archivo:
                cparser.write(archivo)
    else:
        print ('Error 3')
        sys.exit(1)


