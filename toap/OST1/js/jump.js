layui.use(['form', 'layedit', 'laydate'], function(){
	var form = layui.form
	,layer = layui.layer
	,layedit = layui.layedit
	,laydate = layui.laydate;
	//监听提交
//	form.on('submit(index_1)',function(data){
//		window.location.href="index_1.html";
//		return false;
//	});
	form.on('submit(first)',function(data){
		window.location.href="index_1.html";
		return false;
	});
	form.on('submit(second)',function(data){
		window.location.href="second.html";
		return false;
	});
	form.on('submit(third)',function(data){
		window.location.href="third_1.html";
		return false;
	});
	form.on('submit(fourth)',function(data){
		window.location.href="fourth_1.html";
		return false;
	});

});
