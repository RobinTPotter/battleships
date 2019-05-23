/*

"datashover" javascript module to aid converse between WPS and a webpage.

this script is ran in the "head " of an html document, it is a self executing anonymous function 
and defines the functions and properties to a new object "ds" (datashover).

it provides easy means of communication to html page of the java applet datashover class found 
in "DataShover.jar" by takingcare of all the nitty gritty of submitting SAS language and parsing output.

*************************************************************************
THIS IS Event Driven programming - ie. don't use this for programming SAS
*************************************************************************

when placing the java applet in a webpage using an object tag it should be referenced thus:
	
	<object type="application/x-java-applet" id="robin_applet" 
	          style="position:absolute; top:0; left:0; width:10; height:10">
		<param name="archive" value="DataShover.jar" />
		<param name="code" value="DataShover.class" />
		<param name="mayscript" value="yes">
		<param name="scriptable" value="true">
		<param name="callback" value="complete">
		<param name="initialized_callback" value="wpsready">
	</object>

within the script tag in the html body the following links this object with the wps java applet communicator:

	ds.init(document.robin_applet)
		-	see definition below
	complete=ds.complete
		-	the java applet calls the javascript function "complete" when a portion of
			SAS language is submitted so far as i can work out a call to a function 
			outside the base document (ie. the html page) is not allowed so here we set
			"complete" to a reference to the function in the ds object which this code defines

currently, I am not convinced by the order in which submits are performed when the ds.submit(code,callback) 
format is not used. that is to say, callback will be called when the WPS has completed a submit section 
if multiple ds.submit(code,callback) or ds.submit(code) are sent they don't go to a queue as such but 
get "refired" periodically and processed when te wps applet is good and ready.

REMEMBER - this is Event Driven - ie. don't use this for programming SAS!

*/




(function() {
	ds={
		version:'1.0'
	}
	var wps
	/*var callback*/
	var ready=false
	var verbose=false
	ds.init=function(ds_applet,verbose) {
		ds.wps=ds_applet
		ds.wps=ds_applet
		/*ds.callback=callback*/
		ds.ready=true
		ds.verbose=verbose
		return ds.wps
	}
	ds.submit=function(sas) {	
		//ds.addtext('SUBMIT')
		//if (arguments.length>1) for (var xx in arguments) ds.addtext('>>'+arguments[xx])
		if (ds.ready) {
			//ds.addtext(sas)
			ds.ready=false
			ds.wps.submit(sas)	
			if (ds.verbose) ds.addtext('submitted '+sas)
			if (arguments.length>1) { 
				if (ds.verbose) ds.addtext('about to schedule '+arguments[1])
				ds.schedule(arguments[1])
				//ds.addtext('stuck on schedule')
				
			}
		} else { 			
			setTimeout(function() {			
				if (arguments.length>1) ds.submit(sas,arguments.slice(1))
				else ds.submit(sas)
				//ds.submit(arguments)
			},10);  }
			
	}
	ds.complete=function() {
		if (ds.verbose) ds.addtext('done')
		ds.ready=true;
	}
	ds.wpsready=function() {
		if (ds.verbose) ds.addtext('ready')
		ds.ready=true;
	}
	ds.addtext=function(txt) {
		var node=document.createElement('div')
		node.innerHTML=txt+'<br />'
		document.body.appendChild(node)
	}
	ds.getDatasets=function() {
		//ds.addtext('getlib')
		var lib='WORK'
		var str=''
		//alert(arguments[0])
		if (arguments.length>0) {
			lib='_x_'
			str+='libname '+lib+' "'+arguments[0]+'";'			
		}
		ds.wps.clearLogs()
		str+='proc contents data='+lib+'._all_ short out=_test_(keep=memname); run;'
		str+='proc sort data=_test_ nodupkey; by memname; run;'
		str+='data _null_; set _test_ nobs=recs; \n if _n_=1 then put "_" "START_"; \n put memname; \n if _n_=recs then put "_" "END_"; \n run;'
		//str+='data _null_; set _test_ nobs=recs; put memname; run;'
		ds.submit(str,function() {
			//ds.addtext('Hello '+ds.wps.getError())
			var output=''+ds.wps.getError()
			var reg=new RegExp('_START_[^;]+_END_')
			var xx=reg.exec(output).join().split(/\n/)
			var output='['
			for (var x in xx) if (x>0 && x<xx.length-1) {
				if (ds.verbose) ds.addtext(xx[x])
				output+='{dataset:'+xx[x]+'}'
				if (x>1) output+=','
			}
			output+=']'
			return output
		
		})
	}
	ds.getDataset=function(sasdataset,callback) {
		ds.wps.clearLogs()
		var str=''
		
		str+='      option nonotes nonumber; \n'
		str+='      data _temp_; set '+sasdataset+';\n'
		str+='      proc contents data=_temp_ out=_cont_; run; \n'
		str+='      proc sort data=_cont_; by varnum; run; \n'
		str+='      proc sql; \n'
		str+='            select NAME into : _list_ separated by " " from _cont_; \n'
		str+='            select type into : _listt_ separated by " " from _cont_; \n'
		str+='            select varnum into : _liston_ separated by " " from _cont_ where type=1; \n'
		str+='            select varnum into : _listoc_ separated by " " from _cont_ where type ne 1; \n'
		str+='      quit; \n'
		str+='       \n'
		str+='      data _null_; \n'
		str+='      set _temp_ nobs=_recs_; \n'
		str+='      array _varsn_(*) _numeric_ ; \n'
		str+='      array _varsc_(*) _character_ ; \n'
		str+='      array _noms_(%sysfunc(countw(&_list_.))) $100.; \n'
		str+='      array _types_(%sysfunc(countw(&_listt_.))) ; \n'
		str+='      retain _noms_: _types_:; \n'
		str+='      if _n_=1 then do; \n'
		str+='            put "_" "START_" / "[" @; \n'
		str+='            do _i_=1 to dim(_noms_); _noms_(_i_)=scan("&_list_",_i_); _types_(_i_)=scan("&_listt_",_i_); end; \n'
		str+='      end; else put ","; \n'
		str+='      _ic_=1; \n'
		str+='      _in_=1; \n'
		str+='      put "{" @; \n'
		str+='      do _i2_=1 to dim(_noms_); \n'
		str+='            if _i2_ ne 1 then put "," @; \n'
		str+='            if _types_(_i2_)=1 then do; put _noms_(_i2_) ":" _varsn_(_in_) @; _in_=_in_+1; end; \n'
		str+='            else do;  \n'
		str+='                  put _noms_(_i2_) ":""" _varsc_(_ic_) +(-1) """" @; \n'
		str+='                  _ic_=_ic_+1; \n'
		str+='            end; \n'
		str+='      end; \n'
		str+='      put "}" @; \n'
		str+='      if _n_=_recs_ then put "]" /"_" "END_"//; \n'
		str+='      run; \n'
		str+='      option notes; \n'

		
		
		var output
		ds.submit(str,function() {
			if (ds.verbose) ds.addtext('get datasets internal callback')
			output=''+ds.wps.getError()
			output=output.replace(/[\x00-\x1F\x7F]/gi,'')
			output=output.replace(/.*_START_(.+)_END_.*/gi,'$1')
			output=output.replace(/[0-9]+\s+The WPS System\s+[0-9]{1,2}:[0-9]{1,2}\s+[a-z]+,\s+[a-z]+\s+[0-9]{1,2},\s+[0-9]{4}\s{5}/gi,'')
			if (ds.verbose) ds.addtext(output)
			ds.schedule(callback(output))
			
		})
	}
	ds.schedule=function(fun) {
		//ds.addtext('schedule '+ds.ready)
		if (ds.ready) { 
			if (ds.verbose) ds.addtext('scheduled running');
			if (fun!=undefined) fun() 
		} else {
			setTimeout(function() {
				ds.schedule(fun)
			},10);
		}
	}
})();