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
    $('thead').each(function() {
	$(this).append("<tr class='warning no-result'><td colspan='99'><i class='fa fa-warning'></i> No result</td></tr>");
    });
    
    var default_table = "student";
    $('#table-'+default_table).bootstrapTable('refresh', {url: "/api/"+default_table});
   
    $('a[data-toggle="pill"]').on('shown.bs.tab', function(e) {
	var target = $(e.target).attr("href");
	var params = "?" + $(e.target).attr("params");
	target = target.slice(1);
	$('#table-'+target).bootstrapTable('refresh', 
					   {url: "/api/"+target+params});
	    
	$('.search').val('');
	$('.no-result').hide();
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
    $('table').on('load-success.bs.table', function(name) {
	//console.log($(this));
    }); 
    
    
    $(".search").each( function() {
	$(this).keyup(function () {
	    var table = ".results."+$(this).data('id');
	    var searchTerm = $(this).val();
	    var listItem = $(table +' tbody').children('tr');
	    var searchSplit = searchTerm.replace(/ /g, "'):containsi('")
	    
	    $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
		return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
	    }});
	    
	    $(table + " tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
		$(this).attr('visible','false');
	    });
	    
	    $(table + " tbody tr:containsi('" + searchSplit + "')").each(function(e){
		$(this).attr('visible','true');
	    });
	    
	    var jobCount = $(table +' tbody tr[visible="true"]').length;
	    $('.counter').text(jobCount + ' item');
	    
	    if(jobCount == '0') {$('.no-result').show();}
	    else {$('.no-result').hide();}
	});
    });
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
    return value.substring(0, value.indexOf('.') + 2);
}

function expandStudent(i) {
    alert(i);
    console.log("funct");
}
