package kb51_package;
BEGIN { }

$db_login = 'nick';
$db_pass = 'xxxz25t';

$hdd_start_url = "/data/web/html/main";
$system_start_url = "/";
$system_site_url = "http://kb51.ru/new/";
$system_mailimages_url = "";
$captha_sitekey_open = "6LcFFyoUAAAAAAWHfPYxQr9h7475PhdvmLh8aM9l";
$mail_from = 'robot@kb51.ru';
$mail_to = 'kb51@kb51.ru';
$mail_host = 'mail.kb51.ru';
$mail_port = 25;
$mail_username = 'robot';
$mail_password = 'rota6xdb';

sub db_Connect
  {
    $dbh  = DBI->connect("dbi:mysql:site_kb51:localhost:3307", $kb51_package::db_login, $kb51_package::db_pass) or return 'false';
    $dbh->do("set names 'cp1251'");
    return 'true';
  }

sub db_Connect_CP
  {
    my $in_l = shift;
    my $in_p = shift;
    my $in_page = shift;

    $dbh = DBI->connect("dbi:mysql:site_kb51:localhost:3307", $kb51_package::db_login, $kb51_package::db_pass) or return 'false';
    $dbh->do("set names 'cp1251'");
    $res = $kb51_package::dbh->prepare("Select IsAdmin from kb_cp_Login where Nick = '".$in_l."' and Pass=password('".$in_p."') and
                                        IfNull(Date_DisableTo, Now()) <= Now() and IsDeleted is Null;");
    $res->execute();
    $ln = $res->fetchrow_hashref();
    my $IsAdmin = $ln->{'IsAdmin'};
    $res->finish();
    if ($IsAdmin)
      {
        if ($in_page > 0)
          {
            $res = $kb51_package::dbh->prepare("Select l.ID_kb_cp_Login
                                                from kb_cp_Rights r Inner Join kb_cp_Login l On r.ID_kb_cp_Login = l.ID_kb_cp_Login
                                                Where l.Nick = '".$in_l."' and r.ID_kb_cp_Content = ".$in_page." and r.IsDeleted is Null");
            $res->execute();
            $ln = $res->fetchrow_hashref();
            $IsAdmin = $ln->{'ID_kb_cp_Login'};
            $res->finish();
            if ($IsAdmin) { return 'true'; } else { return 'nocontent'; }
          }
        else
          { return 'true'; }
      }
    else
      { return 'nocp'; }
  }

sub db_Connect_MIS
  {
    my $mis_login = 'smith';
    my $mis_pass = 'iicmdwnxa';
#    my $DSN_MIS = "driver={SQL Server};Server=NickPC;database=kb51";
    my $DSN_MIS = "MAINFRAME_MIS2";
    $dbh_mis = DBI->connect("dbi:ODBC:$DSN_MIS", $mis_login, $mis_pass) or return "false";
    $dbh_mis->do("set DateFormat dmy");
    $dbh_mis->do("Set DateFirst 1");

    return 'true';
  }

sub readCookies
  {
    my @cookieArray = split("; ", $ENV{'HTTP_COOKIE'}); 
    my $cookieName;
    my $cookieValue;
    my $cookieHash;

    foreach(@cookieArray)
      {
        ($cookieName, $cookieValue)=split("=", $_);
        $cookieHash{$cookieName} = $cookieValue;
      }
    return %cookieHash;
  }

sub read_input
  {
    local ($temp,@pairs,$censored,$mail_to);
    $censored = "!err!";
    if ($ENV{'REQUEST_METHOD'} eq 'POST')
      {
	read(STDIN,$temp,$ENV{'CONTENT_LENGTH'});
      }
    else
      {
	$temp=$ENV{'QUERY_STRING'};
      }

    if ($temp ne '')
      {
         @pairs=split(/&/,$temp);
         foreach $item(@pairs)
           {
             ($key,$content)=split (/=/,$item,2);    # Split into key and value.
             $data_RUS{$key}=$content; # Associate key and value
             $content=~tr/+/ /; # Convert plus's to spaces
             $content=~ s/%(..)/pack("c",hex($1))/ge;	# Convert %XX from hex numbers to alphanumeric

             # get rid of attempts to insert HTML tags
             if($TagsAllowed !=1)
               {
                 $content =~ s/<([^ >]|\n).*>//gs;
                 $content =~ s/[\<\>]//gs;
               }
             # get rid of attempts to insert illeagl character
             $content =~ s/[\`\*\|\^]/$censored/gs;
             $content=~s/'/&lsquo;/g;

             # get rid of attempts to insert bad tags
             $content=~s/meta/$censored/gi;
	     $content=~s/refresh/$censored/gi;
	     $content=~s/open/$censored/gi;
	     $content=~s/exec/$censored/gi;
	     $content=~s/passwd/$censored/gi;

             #for database support
  	     $content=~s/:://g;
	     $content=~s/\cM/\n/g;	#convert CR to LF
	     $content=~ s/\n\n/<br>/g;
             $content=~ s/\n/<br>/g;
		
	     if($key =~/email/i)	#make sure email address is legal
               {		
                 $mail_to = $content;
                 $mail_to=~/([\w-.]+\@[\w-.]+)/;
                 $content = $1;
                 $EmailAddress = $content;
               }
		
             # Associate key and value
             $data{$key}=$content; # Associate key and value
           }
         return 1;
      }
    else
      {
        return 0;
      }
  }

sub ShowTableMessage
  {
    my $mess = shift;
    print "<table height=100% border=0 cellpadding=5 cellspacing=1 bgcolor=#33CC99><tbody>";
    print "<tr><td bgcolor=#CCFFCC>$mess</td></tr>";
    print "</tbody></table>";
  }

sub ShowTableErrMessage
  {
    my $mess = shift;
    print "<table height=100% border=0 cellpadding=5 cellspacing=1 bgcolor=#FF6666><tbody>";
    print "<tr><td bgcolor=#FFCCCC><font color=#663333>$mess</font></td></tr>";
    print "</tbody></table>";
  }

sub ShowPagesLine
  {
    my $in_pages_cnt = shift;
    my $in_cur_page = shift;
    my $in_url = shift;
    my $in_square_width = shift;
    my $in_Sharp = shift;

    print "<table height=100% width=100% border=0 cellpadding=2 cellspacing=0><tbody><tr>";
    for($i = 1; $i <= $in_pages_cnt; $i++)
      {
        if (($i == 1)||($i == 2)||($i == 3)||
            ($i == $in_pages_cnt - 2)||($i == $in_pages_cnt-1)||($i == $in_pages_cnt)||
            ($i == $in_cur_page)||($i == $in_cur_page - 1)||($i == $in_cur_page + 1)||
            (($i == $in_pages_cnt - 3)&&($in_cur_page == $in_pages_cnt-5))||
            (($i == 4)&&($in_cur_page == 6))
           )
          {
            if (($i == $in_pages_cnt - 2)&&($in_cur_page <= $in_pages_cnt - 6)) { print "<td width=10>...</td><td width=3></td>"; }

            if ($i == $in_cur_page)
              { print "<td width=".$in_square_width." bgcolor=#9fc5dd align=center>".$i; }
            else
              {
                print "<td width=".$in_square_width." bgcolor=#d9ecf8 align=center>";
                print "<a href='".$in_url."&p=".$i.$in_Sharp."'>".$i."</a>";
              }
            print "</td><td width=3></td>";

            if (($i == 3)&&($in_cur_page >= 7)) { print "<td width=10>...</td><td width=3></td>"; }
          }
      }
    print "<td></td></tr></tbody></table>";
  }

sub Hex_to_Rus
  {
    my $v = shift;
    $v=~ s/%(..)/pack("c",hex($1))/ge;	# Convert %XX from hex numbers to alphanumeric
    return $v;
  }

sub Check_Email
  {
    my $Email = shift;
    if ($Email !~ /^[a-zA-Z0-9_\-\.]+\@[a-zA-Z0-9\-]+\.[a-zA-Z\-\.]+$/) { return 'false'; }	
    else { return 'true'; }
  }

sub Check_Date
  {
    my $d = shift;
    if ($d !~ /^[0-3][0-9]\.[0-1][0-9]\.[0-2][0-9][0-9][0-9]$/) { return 'false'; }	
    else { return 'true'; }
  }

sub Check_URL
  {
    my $v = shift;
    if ($v !~ /^[a-zA-Z0-9_\:\/\-\~\.]+$/) { return 'false'; }	
    else { return 'true'; }
  }

sub Check_Numeric
  {
    my $v = shift;
    if ($v !~ /^[0-9]+$/) { return 'false'; }	
    else { return 'true'; }
  }

sub Check_Float
  {
    my $v = shift;
    if ($v !~ /^[0-9\,\.]+$/) { return 'false'; }	
    else { return 'true'; }
  }

sub Check_SimpleString
  {
    my $v = shift;
    if ($v =~ /[\~\@\#\$\%\^\&\*\(\)\+\|\=\[\]\{\}\;\'\:\"\/\<\>\?]+/) { return 'false'; }	
    else { return 'true'; }
  }

sub Check_Password
  {
    my $v = shift;
    if ($v !~ /^[a-zA-Z0-9]+$/) { return 'false'; }	
    else { return 'true'; }
  }

sub Check_Password_Value
  {
    $v = shift;
    if ($v !~ /[0-9]+/) { return 'false'; }	
    elsif ($v !~ /[a-zA-Z]+/) { return 'false'; }	
    else { return 'true'; }
  }

sub Check_BirthDay
  {
    my $d = shift;
    my $m = shift;
    my $y = shift;
    my $res = 'true';

    if (($m > 12) || ($m < 1)) { $res = 'false'; }
    elsif (($m == 1) || ($m == 3) || ($m == 5) || ($m == 7) || ($m == 8) || ($m == 10) || ($m == 12))
      { if (($d > 31) || ($m < 1)) { $res = 'false'; } }
    elsif (($m == 4) || ($m == 6) || ($m == 9) || ($m == 11))
      { if (($d > 30) || ($m < 1)) { $res = 'false'; } }
    elsif ($m == 2)
      { if (($d > 29) || ($m < 1)) { $res = 'false'; } }
    if (($y > 2100) || ($y < 1900)) { $res = 'false'; }
    return $res;
  }

sub Add_Script{
	my $script_path = shift;
	my $charset = shift;

	my $mtime = (stat $folder_Main.$script_path)[9]; 
	print "<script type='text/javascript' src='$script_path?$mtime' charset=$charset ></script>";
	
}
sub Add_CSS{
	my $css_path = shift;

	my $mtime = (stat $folder_Main.$css_path)[9]; 
	print "<LINK href=\"$css_path?$mtime\" type=text/css rel=stylesheet>";
}

sub Show_Page_Header
  {
    my $isneedscripts = shift;
    my $iscp = shift;
    my $islk = shift;
    my $isdeps = shift;
    my $isdoctors = shift;
	my $charset = shift||"windows-1251";


    my $url_prefix = "";
    if (($iscp)||($islk)||($isdeps)||($isdoctors)) { $url_prefix = "../"; }


    print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
           <html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"ru\" xml:lang=\"ru\">";

    print "<head>";

    my $title = "КБ № 51";
    if ($iscp) { print "<title>Панель управления / ".$title."</title>"; }
    elsif ($islk) { print "<title>Личный кабинет / ".$title."</title>"; }
    elsif ($isdeps) { print "<title>Подразделения / ".$title."</title>"; }
    elsif ($isdoctors) { print "<title>Специалисты / ".$title."</title>"; }
    else { print "<title>".$title."</title>"; }

    print "<meta http-equiv=\"Cache-Control\" content=\"no-cache, must-revalidate\">";
    print "<meta http-equiv=\"Pragma\" content=\"no-cache\">";
    print "<meta HTTP-EQUIV=\"Expires\" CONTENT=\"0\">";

    print "<meta charset=\"$charset\">";
    print "<meta http-equiv=\"content-type\" content=\"text/html;charset=$charset\">";
    print "<meta http-equiv=\"Content-language\" content=\"ru\">";
    print "<meta name=\"description\" content=\"Сайт Клинической больницы № 51 ФМБА России г. Железногорск Красноярского края\">";
    Add_CSS($url_prefix."css/layout.css");
	print "<script src='https://www.google.com/recaptcha/api.js'></script>";

    if ($isneedscripts == 1)
      {
        Add_CSS($url_prefix."css/main.css");
        Add_CSS($url_prefix."css/swiper.css");
        Add_Script($url_prefix."js/jquery-1.8.2.min.js",$charset);
        Add_Script($url_prefix."js/swiper.min.js",$charset);
      }
    elsif ($isneedscripts == 2)
      {
        Add_CSS($url_prefix."css/lk.css");
        Add_CSS($url_prefix."css/smartclinic.css");
        Add_Script($url_prefix."js/jquery-1.8.2.min.js",$charset);
        Add_Script($url_prefix."js/swiper.min.js",$charset);
        Add_Script($url_prefix."js/lk.js",$charset);
        Add_Script($url_prefix."js/jquery.maphilight.js",$charset);
      }
    elsif ($isneedscripts == 3)
      {
        Add_CSS($url_prefix."css/main.css");
        Add_CSS($url_prefix."css/deps.css");
        Add_CSS($url_prefix."css/swiper.css");
        Add_Script($url_prefix."js/jquery-1.8.2.min.js",$charset);
        Add_Script($url_prefix."js/swiper.min.js",$charset);
      }
    elsif ($isneedscripts == 4)
      {
        Add_CSS($url_prefix."css/main.css");
        Add_CSS($url_prefix."css/doctors.css");
        Add_Script($url_prefix."js/jquery-1.8.2.min.js",$charset);
      }
    elsif ($isneedscripts == 5)
      {
        Add_CSS($url_prefix."css/main.css");
        Add_CSS($url_prefix."css/news.css");
        Add_Script($url_prefix."js/jquery-1.8.2.min.js",$charset);
      }
    elsif ($isneedscripts == 6)
      {
        Add_CSS($url_prefix."css/main.css");
        Add_CSS($url_prefix."css/digitaldoctor.css");
        Add_Script($url_prefix."js/jquery-1.8.2.min.js",$charset);
      }

	print '<script type="text/javascript" src="//vk.com/js/api/openapi.js?121"></script>';

    print "</head>";
  }

sub Show_Connect_Result
  {
    my $mess = shift;
    my $iscp = shift;
    my $islk = shift;

    my $url_prefix = "";
    if (($iscp)||($islk)) { $url_prefix = "../"; }

    print "Cache-Control: no-cache\n";
    print "Content-Type: text/html\n\n";
    print "<html>";

    Show_Page_Header(0, $iscp, $islk);

    print "<body>";
    print "<table width=100% height=100% border=0 cellpadding=20 cellspacing=0><tbody>";
    print "<tr height=20><td></td></tr>";
    print "<tr height=20><td>".$mess."</td></tr>";
    print "<tr><td></td></tr>";
    print "</tbody></table>";
    print "</body></html>";
  }

sub Show_Connect_Result_NoRights_CP
  {
    my $l = shift;
    my $conres = shift;

    my $err = "";
    if ($conres eq "false") { $err = "Ошибка авторизации. Логин или пароль не верны или заблокированы!"; }
    elsif ($conres eq "nocp") { $err = "Пользователь ".$l." не имеет доступа к панели управления сайтом!45"; }
    elsif ($conres eq "nocontent") { $err = "Пользователь ".$l." не имеет доступа к данному разделу панели управления сайтом!"; }
    if ($err) { $err = $err."<br>Попробуйте начать с <a href='.'>главной</a> страницы"; }
    return $err;
  }

sub Show_ComboBox
  {
    $in_query = shift;
    $in_name = shift;
    $in_id_Main_Query = shift;
    $in_Width = shift;
    $in_Empty_Value = shift;
	$in_Class = shift;
	$in_Group_Column = shift; #Номер колонки для вывода группы

	my $Current_Group;
	
    $res = $kb51_package::dbh->prepare($in_query);
    $res->execute();
    print "<select class='".$in_Class."' name='", $in_name, "' id='".$in_name."' size=1 ".((!$in_Class)?"STYLE='width=".$in_Width.";font-size: 12px;'":"").">";
    if ($in_Empty_Value) { print "<option value='0'>", $in_Empty_Value, "</option>"; }
    while (my @cln = $res->fetchrow_array())
      { 
		if (($in_Group_Column)&&($Current_Group ne $cln[$in_Group_Column])){
		
			print "<optgroup class='".$in_Class."' label='".$cln[$in_Group_Column]."'>";
			$Current_Group = $cln[$in_Group_Column];
		
		}
        if (@cln[0] == $in_id_Main_Query) { $s = "selected"; } else { $s = "" }
        print "<option class='".$in_Class."' ", $s, " value='", @cln[0], "'>", @cln[1], "</option>";
      }
    $res->finish;
    print "</select>";
  }

sub Show_ComboBox_MIS
  {
    my $in_query = shift;
    my $in_name = shift;
    my $in_id_Main_Query = shift;
    my $in_Width = shift;
    my $in_Empty_Value = shift;
	my $in_Class = shift;
	my $in_Group_Column = shift; #Номер колонки для вывода группы
	
	my $Current_Group;

    my $res = $kb51_package::dbh_mis->prepare($in_query);
    $res->execute();

    print "<select class='".$in_Class."' name='", $in_name, "' id='".$in_name."' size=1 ".((!$in_Class)?"STYLE='width=".$in_Width.";font-size: 12px;'":"").">";
    if ($in_Empty_Value) { print "<option value='0'>", $in_Empty_Value, "</option>"; }
    while (my @cln = $res->fetchrow_array())
      { 
		if (($in_Group_Column)&&($Current_Group ne $cln[$in_Group_Column])){
		
			print "<optgroup class='".$in_Class."' label='".$cln[$in_Group_Column]."'>";
			$Current_Group = $cln[$in_Group_Column];
		
		}
        if (@cln[0] == $in_id_Main_Query) { $s = "selected"; } else { $s = "" }
        print "<option class='".$in_Class."' ", $s, " value='", @cln[0], "'>", @cln[1], "</option>";
      }
    $res->finish;
    print "</select>";
  }

sub Show_Top_Panel_Search
  {
    # print "<div class='mainsitesearch'>
           # <table width=100% height=100% border=0 cellpadding=2 cellspacing=0 class='hidden'>
                        # <form method='get' action='.'>
				# <tbody>
					# <tr height=24>
						# <td><input class='editsitesearch' id='ideditsitesearch' type='text' value='Поиск' name='s'></td>
						# <td width=20><input class='btnsitesearch' type=submit value=''></td>
					# </tr>
				# </tbody>
			# </form>
           # </table>
           # </div>";
	print "
		<script>
		  (function() {
			var cx = '010977352645689042075:hws3cw7fc6a';
			var gcse = document.createElement('script');
			gcse.type = 'text/javascript';
			gcse.async = true;
			gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
				'//cse.google.com/cse.js?cx=' + cx;
			var s = document.getElementsByTagName('script')[0];
			s.parentNode.insertBefore(gcse, s);
		  })();
		</script>
		<div class='mainsitesearch'>
		<gcse:searchbox-only></gcse:searchbox-only>
		</div>
	";
  }

sub Check_Captcha{
	my $recaptcha_response  = shift;
	
	use LWP::UserAgent;
	my $ua = LWP::UserAgent->new;
	my $url = "https://www.google.com/recaptcha/api/siteverify";
	my $keys = "secret=6LcFFyoUAAAAAL4neZLtN8S88JlvUlJxNnLz4Ydz&response=".$recaptcha_response;
	
	my $req = HTTP::Request->new(POST=>$url);
	$req->content_type('application/x-www-form-urlencoded');
	$req->content($keys);
	my $res = $ua->request($req);

	use JSON::Parse 'parse_json';
    my $response = parse_json ($res->content);
	use Data::Dumper;
	
	return $response->{'success'};
}

sub Show_Partners {
	my $Result =  "
	<div class='mainpartners'>
		<table border=0 padding=0 width=100%>
			<tr height=30px>
				<td align=center>
					<a href='http://fmbaros.ru' title='ФМБА России'><img src='/images/fmba.png' height=30px/ alt='ФМБА России'></a>
				</td>
				<td align=center>
					<a href='http://medprofedu.ru' title='Институт повышения квалификации ФМБА'><img src='/images/medprofedu.png' height=30px/ alt='Институт повышения квалификации ФМБА'></a>
				</td>
				<td align=center>
					<a href='http://rosminzdrav.ru' title='Министерство здравоохранения РФ'><img src='/images/minzdrav.png' height=30px/ alt='Министерство здравоохранения РФ'></a>
				</td>
				<!-->
				<td align=center>
					<a href='http://pfrf.ru' title='Пенсионный фонд России'><img src='/images/pfr.png' height=30px/ alt='Пенсионный фонд России'></a>
				</td>
				<--!>
				<td align=center>
					<a href='https://urgaps.ru/' title='Уральский институт повышения квалификации и переподготовки'><img src='/images/uripkip.logo.png' height=30px/ alt='Уральский институт повышения квалификации и переподготовки'></a>
				</td>
				<td align=center>
					<a href='http://ffoms.ru' title='Федеральный фонд обязательного медицинского страхования'><img src='/images/ffoms.png' height=30px/ alt='Федеральный фонд обязательного медицинского страхования'></a>
				</td>
			</tr>
			<tr height=30px>
				<td align=center>
					<a href='http://www.nadejdamco.ru/' title='АО МСО Надежда'><img src='/images/nadejda.png' height=30px/ alt='АО МСО Надежда'></a>
				</td>
				<td align=center>
					<a href='http://oms-capitalpolis.ru/' title='СК Капитал-полис'><img src='/images/capital.png' height=30px alt='СК Капитал-полис'/></a>
				</td>
				<td align=center>
					<a href='http://www.mvostok.ru/' title='Медика Восток'><img src='/images/mvostok.png' height=30px/ alt='Медика Восток'></a>
				</td>
				<td align=center>
					<a href='http://vtbms.ru/' title='ВТБ Медицинское страхование'><img src='/images/vtb.png' height=30px/ alt='ВТБ Медицинское страхование'></a>
				</td>
				<td align=center>
					<a href='http://www.ingos-m.ru/' title='СК Ингосстрах-М' ><img src='/images/ingosstrah.png' height=30px/ alt='СК Ингосстрах-М' ></a>
				</td>
			</tr>
		</table>
	</div>
	";
	
	return $Result;
}

sub Show_Social{

	return "
		<script type='text/javascript' src='//vk.com/js/api/openapi.js?121'></script>
		<script type='text/javascript'>
			VK.Widgets.Group('vk_groups', {mode: 1, width: '220', height: '220', color1: 'FFFFFF', color2: '2B587A', color3: '5B7FA6'}, 109396081);
		</script>
		<table width=100% style='top:0px;'>
			<tr>
				<td width=50%>
					<!-- VK_Widget -->
					<div id='vk_groups' class='vk_groups'></div>			
				</td>
				<td width=50% align=center>
					<!-- InstaWidget -->
					<a href='https://www.instagram.com/kb_51_fmba/'><img src='/images/instagram.png' height=120px alt='Иконка инстаграмм' title='Мы в Инстаграм!' /></a>
				</td>
			</tr>
		</table>
	";

}
  return 1;

END { }
