
var mp_swver = 0;
var mp_pos = 0;
var mp_html = "";
if( navigator.mimeTypes && navigator.mimeTypes["application/x-shockwave-flash"] && navigator.mimeTypes["application/x-shockwave-flash"].enabledPlugin ) {
  if( navigator.plugins && navigator.plugins["Shockwave Flash"] ) {
    mp_pos = navigator.plugins["Shockwave Flash"].description.indexOf("Shockwave Flash");
    mp_swver = navigator.plugins["Shockwave Flash"].description.substr(mp_pos+16,1);
  }
} else if ( navigator.userAgent && navigator.userAgent.indexOf("MSIE") >= 0 && ( navigator.userAgent.indexOf("Windows") >= 0 ) ) {
  document.write("<SCR"+"IPT LANGUAGE=VBScript>\n");
  document.write("on error resume next\n");
  document.write("For mp_i=11 To 6 Step -1\n");
  document.write("If Not IsObject(CreateObject(\"ShockwaveFlash.ShockwaveFlash.\" & mp_i)) Then\n");
  document.write("Else\n");
  document.write("  mp_swver=mp_i\n");
  document.write("  Exit For\n");
  document.write("End If\n");
  document.write("Next\n");
  document.write("</SCR"+"IPT> \n");
}
if( mp_swver >= 6 ) {
  mp_html =  "<OBJECT classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\"";
  mp_html += " codebase=\"\" id=\"9810/58350/CG_Never_160X600.\" NAME=\"movie2561265\" WIDTH=\"160\" HEIGHT=\"600\">";
  if( mp_swver > 5 ) {
    mp_html += "<PARAM NAME=FlashVars VALUE=\"clickTAG=http://altfarm.mediaplex.com/ad/ck/9810-58350-23369-0?mpt=546721\">";
    mp_html += "<PARAM NAME=movie VALUE=\"http://img-cdn.mediaplex.com/0/9810/58350/CG_Never_160X600.swf\">";
  } else
    mp_html += "<PARAM NAME=movie VALUE=\"http://img-cdn.mediaplex.com/0/9810/58350/CG_Never_160X600.swf?clickTAG=http://altfarm.mediaplex.com/ad/ck/9810-58350-23369-0?mpt=546721\">";
  mp_html += "<PARAM NAME=wmode VALUE=\"opaque\">";
  if( mp_swver > 5 )
    mp_html += "<EMBED wmode=\"opaque\" NAME=\"9810/58350/CG_Never_160X600.\" src=\"http://img-cdn.mediaplex.com/0/9810/58350/CG_Never_160X600.swf\" FlashVars=\"clickTAG=http://altfarm.mediaplex.com/ad/ck/9810-58350-23369-0?mpt=546721\"";
  else
    mp_html += "<EMBED wmode=\"opaque\" NAME=\"9810/58350/CG_Never_160X600.\" src=\"http://img-cdn.mediaplex.com/0/9810/58350/CG_Never_160X600.swf?clickTAG=http://altfarm.mediaplex.com/ad/ck/9810-58350-23369-0?mpt=546721\"";
  mp_html += " swLiveConnect=\"FALSE\" WIDTH=\"160\" HEIGHT=\"600\" TYPE=\"application/x-shockwave-flash\" PLUGINSPAGE=\"\">";
  mp_html += "</EMBED>";
  mp_html += "</OBJECT>";
  if( window.DocumentWrite )
    DocumentWrite( mp_html );
  else
    document.write( mp_html );
} else if( !( navigator.appName && navigator.appName.indexOf("Netscape") >= 0 && navigator.appVersion.indexOf("2.") >= 0 ) ) {
  document.write("<a href=\"http://altfarm.mediaplex.com/ad/ck/9810-58350-23369-0?mpt=546721\" TARGET=\"_blank\">");
  document.write("<IMG SRC=\"http://img-cdn.mediaplex.com/0/9810/58350/CG_Never_160X600.jpg\" WIDTH=\"160\" HEIGHT=\"600\" BORDER=0></a>");
}
//-->

