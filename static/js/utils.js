//设置cookie，其中expires为天数，直接输入数字即可
function setCookie(_key,_value,_expires,_path,_domain,_secure){
	var _cookie=_key+"="+decodeURIComponent(_value);
	//设置时间
	if (_expires) {
		var dates=new Date();
		dates.setDate(dates.getDate()+_expires);
		_cookie+=";expires="+dates;
	}
//	设置路径
	if (_path) {
		_cookie+=";path="+_path;
	}
	// 设置语句
	if (_domain) {
		_cookie+=";domain="+_domain;
	}
	if (_secure) {
		_secure=true;
		_cookie+=";secure="+_secure;
	}
	document.cookie=_cookie;
}
//获取cookie
function getCookie(_key){
	var list=document.cookie;
	_key=list.indexOf(_key)==0?(_key+"="):("; "+_key+"=");
	//查找key的位置
	var _index=list.indexOf(_key);
	if(_index==-1){
		return null;
	}
	//设置键所属的值的起始点
	var cookieStart=_index+_key.length;
	//设置键所属的值的终点
	var cookieEnd=list.indexOf(";",cookieStart)==-1?(list.length):(list.indexOf(";",cookieStart));
	return decodeURIComponent(list.substring(cookieStart,cookieEnd));
}

//删除cookie
function delCookie(_key,_path){
    if (!_path) {
        _path="/"
    }
	setCookie(_key,"",-1000, _path);
}