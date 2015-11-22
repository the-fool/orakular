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
    initCourseListTable();
    $('#student-list').on('hidden.bs.modal', function(e) {
       $(this).find('.form-control').val('').trigger('keyup');
       $(this).find('.confirm').prop('disabled', true);
    });

    $('#tab-current-enrollment .nav-tabs > li > a').first().trigger('click');

}); // end document.ready()

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


}
