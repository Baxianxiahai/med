layui.use(['form', 'layedit', 'laydate'], function(){
	var form = layui.form
	,layer = layui.layer
	,layedit = layui.layedit
	,laydate = layui.laydate;
	//监听提交
	form.on('submit(index_1)',function(data){
		window.location.href="index.html";
		return false;
	});
	form.on('submit(lumbago)',function(data){
		window.location.href="lumbago_1.html";
		return false;
	});
	form.on('submit(balance)',function(data){
		window.location.href="balance.html";
		return false;
	});
	form.on('submit(SF-36)',function(data){
		window.location.href="SF_36_1.html";
		return false;
	});
	form.on('submit(picture)',function(data){
		window.location.href="common_5.html";
		return false;
	});

});