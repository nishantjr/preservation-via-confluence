#!/usr/bin/env python3

from kninja import *
import sys
import os.path

proj = KProject()
lambda_k = proj.source('lambda.md').then(proj.tangle().output(proj.tangleddir('lambda.k')))

types = lambda_k \
            .then(proj.kompile(backend = 'java')
                      .variables( directory = proj.builddir('types')
                                , flags = '--main-module TYPES --syntax-module LAMBDA-SYNTAX'
                                )
                 ).default()
exec = lambda_k \
             .then(proj.kompile(backend = 'java') \
                      .variables( directory = proj.builddir('exec')
                               , flags = '--main-module EXEC --syntax-module LAMBDA-SYNTAX'
                               )
                 ).default()

def do_test(defn, pattern, input):
    expected = input + '.out'
    return proj.source(input) \
              .then(defn.krun().variables(flags = '--search --pattern "{}"'.format(pattern))) \
              .then(proj.check(expected)) \
              .default()

def typing_test(input):
    return do_test(types, '<k> V:K </k>', input)
def exec_test(input):
    return do_test(exec, '<k> V:K </k>', input)

typing_test('t/types/factorial-letrec.lambda')
typing_test('t/types/ll.lambda')

exec_test('t/exec/arithmetic-div-zero.lambda')
exec_test('t/exec/arithmetic.lambda')
# exec_test('t/exec/closed-variable-capture.lambda') # w         cannot be typed
# exec_test('t/exec/factorial-let-fix.lambda')       # fix/Omega cannot be typed
# exec_test('t/exec/factorial-let.lambda')           # fix       cannot be typed
exec_test('t/exec/factorial-letrec.lambda')
exec_test('t/exec/fibbo.lambda')
exec_test('t/exec/free-variable-capture.lambda')
exec_test('t/exec/identity.lambda')
exec_test('t/exec/if.lambda')
exec_test('t/exec/lets.lambda')
