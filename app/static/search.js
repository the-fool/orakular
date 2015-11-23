function initMainTables() {
    initDepartmentTable();
    initFacultyTable();
    initEnrollmentTable();
    initStudentTable();
    initCourseTable();
}
function initDepartmentTable() {
    var $table = $('#table-department');
    $table.bootstrapTable({
	cache: false,
	url: '/api/department',
	detailView: true,
	showRefresh: true,
	local: 'en-US',
	search: true,
	columns: [
	    {
		title: 'ID',
		field: 'did',
		align: 'center',
		sortable: true
	    },{
		title: 'Name',
		field: 'dname',
		align: 'center',
		sortable: true
	    }
	]
    });
}

function initFacultyTable() {
    var $table = $('#table-faculty');
    $table.bootstrapTable({
	cache: false,
	url: '/api/faculty',
	showMultiSort: true,
	search: true,
	detailView: true,
	showRefresh: true,
	locale: 'en-US',
	columns:[
            {
                title: 'ID',
                field: 'fid',
                align: 'center',
                sortable: true

            }, {
                title: 'Name',
                field: 'fname',
                align: 'center',
                sortable: true

            }, {
                title: 'Dep. ID',
                field: 'deptid',
                align: 'center',
                sortable: true,
	    }
	]
    });
}

function initEnrollmentTable() {
    var $table = $('#table-enrolled');
    $table.bootstrapTable({
        cache: false,
        url: '/api/enrolled?s_avg=true',
        showMultiSort: true,
	search: true,
	detailView: true,
        columns: [
            {
                title: 'Course ID',
                field: 'cid',
                align: 'center',
                sortable: true
            }, {
	        title: 'SID',
                field: 'sid',
                align: 'center',
                sortable: true
            }, {
                title: 'Exam 1',
                field: 'exam1',
                align: 'center',
                sortable: true
            }, {
                title: 'Exam 2',
                field: 'exam2',
                align: 'center',
                sortable: true
            }, {
                title: 'Final',
                field: 'final',
                align: 'center',
		sortable: true,
	    }, {
		title: 'Average',
                field: 'avg',
                align: 'center',
		formatter: floatFormat,
		sortable: true,
	    }
	]
    });
}
function initCourseTable() {
    var $table=$('#table-course');
    $table.bootstrapTable({
        cache: false,
        search: true,
	showRefresh: true,
	showMultiSort: true,
        url: '/api/course?join=Faculty',
        columns: [
            {
                title: 'Course ID',
                field: 'cid',
                align: 'center',
                sortable: true
            }, {
                title: 'Name',
                field: 'cname',
                align: 'center',
                sortable: true,
            }, {
                title: 'When',
                field: 'meets_at',
                align: 'center',
                sortable: true,
            },  {
                title: 'Room',
                field: 'room',
                align: 'center',
                sortable: true,
            }, {
                title: 'Limit',
                field: 'limit',
                align: 'center',
                sortable: true,
           }, {
                title: 'Active',
                field: 'active',
                align: 'center',
                sortable: true,
           }, {
                title: 'Professor ID',
                sortable: true,
                field: 'fid',
                align: 'center'
	   }, {
	       title: 'Professor Name',
                sortable: true,
                field: 'fname',
                align: 'center'
	   }
	]
    });
}
			 
function initStudentTable() {
    var $table = $('#table-student')
    $table.bootstrapTable({
        cache: false,
	url: "/api/student",
        showMultiSort: true,
	detailView: true,
        search: true,

        columns: [
            {
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
		sorter: levelSorter,
                align: 'center',
                sortable: true
            }, {
		title: 'Age',
		field: 'age',
		align: 'center',
		sortable: true
	    }
	]
    });
}

function expandDepartmentSub($el, row) {
   columns= [{
	field: 'cid',
	title: 'Course ID'
    }, {
	field: 'cname',
	title: 'Course Name',
    }, {
	field: 'meets_at',
	title: 'When'
    },{
	field: 'room',
	title: 'Where'
    }, {
	field: 'fid',
	title: 'Faculty ID'
    }, {
	field: 'fname',
	title: 'Faculty Name'
    }, {
	field: 'c_avg',
	title: 'Course Avg',
	formatter: 'floatFormat'
    }];

    url = '/api/course?c_avg=true&join=Faculty&filter=deptid_'+row['did'];
    $el.html('<table></table>').find('table').bootstrapTable({
	columns: columns,
	url: url,
	classes: 'table no-hover'
    });
}
function expandFacultySub($el, row) {
    columns= [{
	field: 'cid',
	title: 'Course ID'
    }, {
	field: 'cname',
	title: 'Course Name',
    }, {
	field: 'meets_at',
	title: 'When'
    },{
	field: 'room',
	title: 'Where'
    }, {
	field: 'c_avg',
	title: 'Course Avg',
	formatter: 'floatFormat'
    }];

    url = '/api/course?c_avg=true&filter=fid_'+row['fid'];
    $el.html('<table></table>').find('table').bootstrapTable({
	columns: columns,
	url: url,
	classes: 'table no-hover'
    });
}
function expandStudentSub($el, row) {
    columns= [{
	field: 'cid',
	title: 'Courses'
    }, {
	field: 'exam1',
	title: 'Exam 1',
    }, {
	field: 'exam2',
	title: 'Exam 2'
    },{
	field: 'final',
	title: 'Final'
    }, {
	field: 'avg',
	title: 'Course Avg',
	formatter: 'floatFormat'
    }];

    url = '/api/enrolled?s_avg=true&filter=sid_'+row['sid'];
    $el.html('<table></table>').find('table').bootstrapTable({
	columns: columns,
	url: url,
	classes: 'table no-hover'
    });
}
function expandCourseSub($el, row) {
    columns = [{
	field: 'sid',
	title: 'Student ID'
    }, {
	field: 'sname',
	title: 'Student Name'
    }, {
	field: 'exam1',
	title: 'Exam 1',
    }, {
	field: 'exam2',
	title: 'Exam 2'
    },{
	field: 'final',
	title: 'Final'
    }, {
	field: 'avg',
	title: 'Course Avg',
	formatter: 'floatFormat'
    }];
    
    
    url = '/api/enrolled?s_avg=true&join=Student&filter=cid_'+row['cid'];
    $el.html('<table></table>').find('table').bootstrapTable({
	classes: 'table table-striped no-hover',
	columns: columns,
	url: url
    });	
}

$(document).ready(function () {
    var default_table = "student";
//    $('#table-'+default_table).bootstrapTable('refresh', {url: "/api/"+default_table});
   
    $('a[data-toggle="pill"]').on('shown.bs.tab', function(e) {
	var target = $(e.target).attr("href");
	var params = "?" + $(e.target).attr("params");
	target = target.slice(1);
	$('#table-'+target).bootstrapTable('refresh');
    });
    
    $('table').on('expand-row.bs.table', function(e, index, row, $detail) {
	switch ($('div.tab-content > .active.in').attr('id')) {
	    case "student": expandStudentSub($detail, row); break;
	    case "course": expandCourseSub($detail, row); break;
	    case "faculty": expandFacultySub($detail, row); break;
	    case "department": expandDepartmentSub($detail, row); break;
	    default: console.log("default");
	}
    });
    $('table').on('click-row.bs.table', function(e,row,$tr) {
	$tr.find('>td>.detail-icon').trigger('click');
    });
    initMainTables();
});

function levelSorter(a, b) {
    var levels = { "Freshman":0, "Sophomore":1, "Junior":2, "Senior":3 };
    
    if (levels[a] > levels[b]) return 1;
    if (levels[a] < levels[b]) return -1;
    return 0;
}

function integerFormat(value) {
    return Math.trunc(value);
}
function floatFormat(value) {
    if (value !== undefined) {
	return value.substring(0, value.indexOf('.') + 2);
    }
}

function searchableRow(row, index) {
    return {};
}
