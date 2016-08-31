#!/usr/bin/env python

import os
import binascii
import dill 
import time
import datetime


class Queue:
	def __init__( self, path="/tmp" ):
		self.path = path
		if not os.path.exists( self.path ):
			os.mkdir( self.path )

	def submit( self, function, args ):
		token = binascii.b2a_hex( os.urandom(8) ).decode("utf-8")
		path = os.path.join( self.path, token )
		os.mkdir( path )
		dill.dump( function, open( os.path.join( path, "function" ), "wb" ) ) 
		dill.dump( args, open( os.path.join( path, "args" ) , "wb" ) ) 
		f = open( os.path.join( path, "QUEUED" ), "wb" ) 
		f.close()
		return token

	def status( self, token ):
		path = os.path.join( self.path, token ) 
		if os.path.exists( os.path.join( path, "ERROR" ) ):
			return "ERROR"
		if os.path.exists( os.path.join( path, "FINISHED" ) ):
			return "FINISHED"
		if os.path.exists( os.path.join( path, "RUNNING" ) ):
			return "RUNNING"
		if os.path.exists( os.path.join( path, "QUEUED" ) ):
			return "QUEUED"
		return "UNKNOWN"

	def results( self, token ):
		if self.status( token ) != "FINISHED":
			raise Exception("Job not finished")

		try:
			path = os.path.join( self.path, token ) 
			result  = dill.load( open( os.path.join( path, "results" ), "rb" ) )
			return result
		except:
			raise Exception( "No results" )

	def last_processed( self ):
			f = open( os.path.join( self.path, "last_processed" ), "rb" )
			ret = dill.load( f )
			f.close()
			return ret

	def process( self ):
		while 1:
			for token in os.listdir( self.path ):
				d = os.path.join( self.path, token )
				if os.path.exists( os.path.join( d, "QUEUED" ) ):
					if not os.path.exists( os.path.join( d, "FINISHED" ) ):
						try:
							function = dill.load( open( os.path.join( d, "function" ), "rb" ) )
							args     = dill.load( open( os.path.join( d, "args" ), "rb" ) )

							f = open( os.path.join( d, "RUNNING" ), "wb" )
							f.close()
							print( "Running job [%s]" % ( token ) )
							result = function( args )
							dill.dump( result, open( os.path.join( d, "results" ), "wb" ) )
							print( "\tFinished OK" );
						except :
							print( "\tFinished Error" );
							f = open( os.path.join( d, "ERROR" ), "wb" )
							f.close()

						f = open( os.path.join( d, "FINISHED" ), "wb" )
						f.close()
			f = open( os.path.join( self.path, "last_processed" ), "wb" )
			dill.dump( datetime.datetime.now(), f )
			f.close()

		time.sleep(5)


import sys


def do_stuff( args ):
	r=[]	
	for a in args:
		r.append( a+1 )
	return r

if __name__ == "__main__":
	if( len(sys.argv) > 1 and sys.argv[1] == "--worker" ):
		print("Running worker")
		q = Queue()
		q.process()

	q = Queue()

	for i in range(10):
		token = q.submit( do_stuff, [ 1,2,3,4 ] )
		print(token)
		while q.status( token ) == "QUEUED" or q.status( token ) == "RUNNING":
			print( "%s at %s" % ( q.status(token), q.last_processed() ) )
			time.sleep(1)
		ret = q.results( token )
		print(ret)
