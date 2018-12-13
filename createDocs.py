#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#==============================================================================
# createDocs - Script to create a documentation file.
# Copyright (C) 2018  Oliver Clemens
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#==============================================================================

import re

# Init variables.
currentHeader = None
currentFunction = None
currentText = ''

# Init pattern for end of function.
functionPattern = re.compile(r'\(')

# Open src file and doc file.
with open(r'aviationFormula\aviationFormula.py') as srcFile:
    with open(r'documentation.md','w') as docFile:
        for li in srcFile:
            lineStrip = li.strip()
            if lineStrip.startswith('##'):
                # Save header.
                currentHeader = lineStrip.replace('##','').strip()
            elif lineStrip.startswith('#') and currentHeader is not None:
                # Save text line.
                currentText = '{}{}\n'.format(currentText,lineStrip.replace('#','').strip())
            elif lineStrip.startswith('def'):
                # Get function name
                lineStrip = lineStrip.replace('def','').strip()
                functionEnd = functionPattern.search(lineStrip)
                currentFunction = lineStrip[:functionEnd.end()-1]
                
                # Write stored function information to file.
                docFile.write('## {}\n'.format(currentFunction))
                docFile.write('{}\n\n'.format(currentHeader))
                if currentText:
                    docFile.write('{}\n\n'.format(currentText))
                
                # Restore vars.
                currentHeader = None
                currentFunction = None
                currentText = ''