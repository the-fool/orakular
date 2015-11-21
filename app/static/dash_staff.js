$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
	var target = $(e.target).attr("href");
	var cid = target.split('-')[1];

	var $table = $('#table-'+cid);
	var $remove = $('#remove-'+cid);    
	var selections = [];
	
	function initTable() {
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
	} // end initTable()
	$table.on('check.bs.table uncheck.bs.table ' +
                'check-all.bs.table uncheck-all.bs.table', function () {

		    $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
		    selections = getIdSelections();
		    console.log('checked');
		    console.log(selections);
                });
	$table.on('all.bs.table', function (e, name, args) {
            console.log(name, args);
	});

	$table.on('load-success.bs.table', function() {
	    console.log("success");
	});

	$remove.click(function () {
            var ids = getIdSelections();
	    var parms = cid.concat('_', ids.join('&'));
            $.ajax({
		url: '/api/update/course',
		method: 'DELETE',
		data: cid.concat(ids,'&'),
		success: function(d,s) {
		    console.log('data: '+d);
		    $table.bootstrapTable('remove', {
			 field: 'sid',
			 values: ids
		    });
		    $remove.prop('disabled', true);
		},
		error: function() {
		    console.log("error?");
		}
	    });
	   
        });

	function getIdSelections() {
            return $.map($table.bootstrapTable('getSelections'), function (row) {
		return row['sid'];
            });
	}
	setTimeout(function () {
	    initTable();
        }, 200);

	
    });
    
    $('.nav-tabs > li > a').first().trigger('click');
    
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
