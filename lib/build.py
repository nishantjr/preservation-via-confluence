#!/usr/bin/env python3

from kninja import *
import sys
import os.path

proj = KProject()
lambda_k = proj.source('lambda.md').then(proj.tangle().output(proj.tangleddir('lambda.k')))

lambda_def = lambda_k \
    .then(proj.kompile(backend = 'java') \
              .variables( directory = proj.builddir('exec')
                        , flags = '--main-module LAMBDA-COMBINED --syntax-module LAMBDA-SYNTAX'
                        )
         ).default()

proj.source('unit-tests.md') \
    .then(proj.tangle().output(proj.tangleddir('unit-tests-spec.k'))) \
    .then(lambda_def.kprove()) \
    .then(proj.check('/dev/null')) \
    .alias('unit-tests') \
    .default()
