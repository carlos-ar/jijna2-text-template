#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 22:32:53 2020

@author: carlosar
"""
import os
import jinja2
import pandas as pd
from helpers import delete_files


# import data
input_excel = pd.read_excel('google_form_feedback.xlsx')

# some pandas indexing (subsetting in R) to get data
## first we get all the reviewees names
reviewees = input_excel.iloc[:,2]
## then we return a series with no repetition (the unique function)
reviewee = pd.unique(reviewees)

# setting up jinja2 templating environment
# using default options
txt_jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )

# now, we load our template text file
feedback_template = txt_jinja_env.get_template('./feedback_template.txt')

# set up output directory
outdir = './out_txt_files'
# use a helper that lists all the files in the `out_txt_files` directory
# and deletes them, look in the helpers module for details and 
# link to the stack overflow page
delete_files(outdir)

# here we are going to loop through each unique reviewee
for r in reviewee:
    
    # I only want the data that comes from the current reviewer out of all
    # the reviewers; in my loop, I assign this variable 'r' for the current
    # reviewer
    
    # here is pandas syntax for getting only when my input_excel variable
    # is equal to my current reviewer
    cur_df = input_excel[input_excel.iloc[:,2]==r]
    
    # printing data so I can just inspect and feel confident my loop
    # does what I want it to do
    print(cur_df.iloc[:,1:3])
    
    # now here is more looping per row
    # since each row in my data frame (cur_df) has all the data I want, I loop
    # through each row by using the function dataframe.iterrow() which returns
    # the index of the row and the entire row as well
    for index, row in cur_df.iterrows():
        
        # now, I use jinja2 render to write the text to the template
        # in my template, the variables {{ student }}, {{ reviewee }}, etc
        # are all replaced with the dataframe column corresponding to the value
        # I didn't want to deal with spaces so I just used the column number
        # Note: python indexing begins at zero, so row[0] is the first column
        # in my current row that I am looping from. And row, is a collection
        # of columns
        feedback_writer = feedback_template.render(student_name=row[1],
                                                   reviewee_student=row[2],
                                                   affirm=row[3],
                                                   design=row[4])
                                       
        
        # write everything to files
        fname = os.path.join(outdir, r+'.txt')
        with open(fname,'a') as output:
            output.write(feedback_writer)
