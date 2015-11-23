$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
	var target = $(e.target).attr("href");
	var cid = target.split('-')[1];

	var $table = $('#table-'+cid);
	var $remove = $('#remove-'+cid);    
	var $add = $('#add-'+cid);
	var selections = [];
	
	function initEnrollmentTable() {
	    $table.bootstrapTable({
		cache: false,
		url: '/api/enrolled?join=Student&filter=cid_'+cid,
		idField: 'sid',
		idField2: 'cid',
		columns: [
		  {
                    field: 'state',
                    checkbox: true,
                    align: 'center'
                  }, {
                    title: 'SID',
                    field: 'sid',
                    align: 'center',
                    sortable: true
                }, {
                    title: 'Name',
                    field: 'sname',
                    align: 'center',
		    sortable: true
		}, {
                    title: 'Major',
                    field: 'major',
                    align: 'center',
		    sortable: true
		}, { 
		    title: 'Level',
                    field: 's_level',
                    align: 'center',
		    sortable: true
		},{
                    field: 'exam1',
                    title: 'Exam 1',
                    sortable: true,
                    align: 'center',
                    editable: {
			type: 'text',
			title: 'Exam 1',
			validate: gradeValidate,
			url: '/staff/edit_grade',
			name: 'exam1'
		    }
                    
		}, {
		    field: 'exam2',
                    title: 'Exam 2',
                    sortable: true,
                    align: 'center',
                    editable: {
			type: 'text',
			title: 'Exam 2',
			validate: gradeValidate,
			url: '/staff/edit_grade',
			name: 'exam2'
		    }
                }, {
		    field: 'final',
                    title: 'Final',
                    sortable: true,
                    align: 'center',
                    editable: {
			type: 'text',
			title: 'Final',
			validate: gradeValidate,
			url: '/staff/edit_grade',
			name: 'final'
		    }
		}]
            });
	} // end initEnrollmentTable()
	$table.on('check.bs.table uncheck.bs.table ' +
                'check-all.bs.table uncheck-all.bs.table', function () {
		    $add.prop('disabled', $table.bootstrapTable('getSelections').length);
		    $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
		    selections = getIdSelections();
		});
	$table.on('all.bs.table', function (e, name, args) {
            console.log(name, args);
	});


	$remove.click(function () {
            var data = {'cid': cid, 'sid': getIdSelections()};
	    
            $.ajax({
		url: '/api/update/enrolled',
	
		contentType: 'application/json',
		method: 'DELETE',
		data: JSON.stringify(data),
		success: function(d,s) {
		    console.log('data: '+d);
		    $table.bootstrapTable('remove', {
			 field: 'sid',
			 values: data['sid']
		    });
		    $remove.prop('disabled', true);
		    $add.prop('disabled', false);
		},
		error: function() {
		    console.log("error?");
		}
	    });
        });
	$add.click(function() {
	    var $modal = $('#student-list');
	    var $table = $('#student-list-table');
	    var $confirm = $modal.find('.confirm');
	    $modal.find('.modal-header > h4').text('Select Students to Enroll in ' + cid);
	    $table.bootstrapTable('refresh', 
				  { url: '/api/student?not=true&filter=cid_'+cid }
				 );
	    $confirm.off('click').click(function() {
		var data = {'cid': cid, 'sid':$table.data('selections')};
		console.log(JSON.stringify(data));
		$.ajax({
		    dataType: 'json',
		    contentType: 'application/json',
		    url: '/api/update/enrolled',
		    method: 'POST',
		    data: JSON.stringify(data),
		    success: function(d, s) {
			if (d.length != 0) {
			    var msg = "Schedule conflicts for: \n";
			    d.forEach(function(e) {
				msg = msg.concat('Student ', e['sid'], 
						 ' with course ', e['cid'], '.\n'); 
			    });
			alert(msg);
			}
		    }
		});
		$('#table-'+cid).bootstrapTable('refresh');
		$modal.modal('hide');
	    });
	    
	});

	function getIdSelections() {
            return $.map($table.bootstrapTable('getSelections'), function (row) {
		return row['sid'];
            });
	}
	setTimeout(function () {
	    initEnrollmentTable();
        }, 200);
    }); // end current_course tables
    
    initStudentListTable();
    initCurrentCoursesTable();
    initPersonnelTable();
    $('#student-list').on('hidden.bs.modal', function(e) {
       $(this).find('.form-control').val('').trigger('keyup');
       $(this).find('.confirm').prop('disabled', true);
    });

    $('#tab-current-enrollment .nav-tabs > li > a').first().trigger('click');

}); // end document.ready()

function initStudentListTable() {
    var $table=$('#student-list-table');
    var $confirm=$('#student-list').find('.confirm');
    var selections = [];

    $('#student-list-table').bootstrapTable({
	cache: false,
	height: 350,
	id: 'sid',
	
	columns: [
	    {
		field: 'state',
		checkbox: true,
		align: 'center'
	    }, {
		title: 'SID',
		field: 'sid',
		align: 'center',
		sortable: true
	    }, {
		title: 'Name',
		field: 'sname',
		align: 'center',
		sortable: true
	    }, {
		title: 'Major',
		field: 'major',
		align: 'center',
		sortable: true
	    }, { 
		title: 'Level',
		field: 's_level',
		align: 'center',
		sortable: true
	    }]
	});
    
    $table.on('check.bs.table uncheck.bs.table ' +
              'check-all.bs.table uncheck-all.bs.table', function () {
		  $confirm.prop('disabled', !$table.bootstrapTable('getSelections').length);
		  $table.data('selections', getIdSelections());

              });

    function getIdSelections() {
        return $.map($table.bootstrapTable('getSelections'), function (row) {
	    return row['sid'];
        });
    }
}

function initCurrentCoursesTable() {
    var did = $('#tab-current-courses').data('id');
    
    var $table = $('#table-current-courses');
    var $remove = $('#remove-course');    
    var $add = $('#add-course');
    var selections = [];
    
   
    $table.bootstrapTable({
	cache: false,
	search: true,
	url: '/api/course?join=Faculty&filter=deptid_'+did,
	idField: 'cid',
	columns: [
	    {
                field: 'state',
                checkbox: true,
                align: 'center'
            }, {
                title: 'Course ID',
                field: 'cid',
                align: 'center',
                sortable: true
		
            }, {
                title: 'Name',
                field: 'cname',
                align: 'center',
		sortable: true,
		editable: {
		    type: 'text',
		    title: 'Change Course Name',
		    validate: stringValidate,
		    url: '/staff/update_course',
		    name: 'cname'
		}
	    }, {
                title: 'When',
                field: 'meets_at',
                align: 'center',
		sortable: true,
		editable: {
		    type: 'text',
		    title: 'Change Meeting Time',
		    validate: timeValidate,
		    url: '/staff/update_course',
		    name: 'meets_at'
		}
		
	    }, { 
		title: 'Room',
                field: 'room',
                align: 'center',
		sortable: true,
		editable: {
		    type: 'text',
		    title: 'Change Room',
		    validate: stringValidate,
		    url: '/staff/update_course',
		    name: 'room',
		
		}
	    }, {
		title: 'Limit',
                field: 'limit',
                align: 'center',
		sortable: true,
		editable: {
		    type: 'text',
		    title: 'Set Limit',
		    validate: stringValidate,
		    url: '/staff/update_course',
		    name: 'limit',


		}
	   }, {
		title: 'Professor',
                sortable: true,
		field: 'fid',
                align: 'center',
                editable: {
		    name: 'fid',
		    type: 'select',
		    emptytext: 'Select Professor',
		    defaultValue: 'Select Professor',
		    
		    source:  '/api/faculty?xedit=true&filter=deptid_'+did,
		    sourceCache: false,
		    title: 'Change Professor',
		    url: '/staff/update_course',
		    name: 'fid',
		
		}
            }
	]
    });
    
    $table.on('check.bs.table uncheck.bs.table ' +
              'check-all.bs.table uncheck-all.bs.table', function () {
		  $add.prop('disabled', $table.bootstrapTable('getSelections').length);
		  $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
		  selections = getIdSelections();
	      });
    $table.on('all.bs.table', function (e, name, args) {
        console.log(name, args);
    });
    
    
    $remove.click(function () {
        var data = {'cid': getIdSelections()};
	
        $.ajax({
	    url: '/api/update/course',
	    
	    contentType: 'application/json',
	    method: 'DELETE',
	    data: JSON.stringify(data),
	    success: function(d,s) {
		console.log('data: '+d);
		$table.bootstrapTable('remove', {
		    field: 'cid',
		    values: data['cid']
		});
		data['cid'].forEach(function(e) {
		    console.log("attempting removal of "+e);
		    $('a[href="#tab-'+e+'"]').parent().remove();
		    $('#tab-'+e).remove();
		    $('#tab-current-enrollment .nav-tabs > li > a').first().trigger('click');
		});
		$remove.prop('disabled', true);
		$add.prop('disabled', false);
	    },
	    error: function() {
		console.log("error on delete ajax");
	    }
	});
    });
	
    function getIdSelections() {
        return $.map($table.bootstrapTable('getSelections'), function (row) {
	    return row['cid'];
        });
    }  
   
    
} // end init_current_course

function initPersonnelTable() {
    var did = $('#tab-personnel').data('id');
    
    var $table = $('#table-personnel');
    var $remove = $('#fire');    
    var $add = $('#hire');
    var selections = [];
    
   
    $table.bootstrapTable({
	cache: false,
	url: '/api/personnel?filter=deptid_'+did,
	idField: 'id',
	search: true,
	columns: [
	    {
                field: 'state',
                checkbox: true,
                align: 'center'
            }, {
                title: 'ID',
                field: 'id',
                align: 'center',
                sortable: true
		
            }, {
                title: 'Role',
                field: 'role',
                align: 'center',
                sortable: true
		
            }, {
                title: 'Name',
                field: 'name',
                align: 'center',
		sortable: true,
		editable: {
		    type: 'text',
		    title: 'Change Personnel Name',
		    validate: stringValidate,
		    url: '/staff/update_personnel',
		    name: 'name'
		}
	    }
	]
    });
    
    $table.on('check.bs.table uncheck.bs.table ' +
              'check-all.bs.table uncheck-all.bs.table', function () {
		  $add.prop('disabled', $table.bootstrapTable('getSelections').length);
		  $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
		  selections = getIdSelections();
	      });
    $table.on('all.bs.table', function (e, name, args) {
        console.log(name, args);
    });
    
    
    $remove.click(function () {
        var data = getIdSelections();
	var ids = data.map(function(d) {
	   return d['id'];
	});
	console.log(data);
        $.ajax({
	    url: '/api/update/personnel',
	    
	    contentType: 'application/json',
	    method: 'DELETE',
	    data: JSON.stringify(data),
	    success: function(d,s) {
		console.log('data: '+d);
		$table.bootstrapTable('remove', {
		    field: 'id',
		    values: ids
		});
		$remove.prop('disabled', true);
		$add.prop('disabled', false);
	    },
	    error: function() {
		console.log("error on delete ajax");
	    }
	});
    });
	
    function getIdSelections() {
        return $.map($table.bootstrapTable('getSelections'), function (row) {
	    return {role: row['role'], id: row['id']};
        });
    }  
   
    
} // end initPersonnel

function gradeValidate(value) {
    if($.trim(value) == '') {
        return 'This field is required';
    }
    if($.isNumeric(value)) {
        if (value > 100 || value < 0) {
            return 'Must be between 0 and 100';
        }
    }
    else {
        return 'Must enter a number';
    }
}

function stringValidate(value) {
    if($.trim(value) == '') {
	return 'This field is required';
    }
    if(value.length > 50) {
	return 'Must be less than 50 characters';
    }
}
function profValidate(value) {
    if($.trim(value) == '') {
	return 'This field is required';
    }
}
function timeValidate(value) {
    if($.trim(value) == '') {
	return 'This field is required';
    }
    var pat = /( (M)|(Tu)|(W)|(Th)|(F) )\s([01]\d|2[0-3]):?([0-5]\d)-([01]\d|2[0-3]):?([0-5]\d)/i
    if (!pat.test(value)) {
	return 'Field must be form of MTuWThF 00:00-24:00'
    }

}
