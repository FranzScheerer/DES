<!DOCTYPE html>
<html>
<body>

<h2>Use JavaScript to calculate Spritz hash</h2>
<p>This example writes "Hello JavaScript!" and the hash value into an HTML element with id="demo":</p>

<p id="demo">Ein Test!</p>

<script>
var a = 0, i = 0, j = 0, w = 1, s = [256], out = [32];

function update()
{
    i = (i + w) % 256
    j = s[(j + s[i]) % 256]
    tmp = s[i]
    s[i] = s[j]
    s[j] = tmp
}

function shuffle()
{
    for (v = 0; v < 256; v++) 
        update()
    w = (w + 2) % 256
    a = 0
}

function absorb_nibble(x)
{
    shuffle()
    shuffle()
    shuffle()
    tmp = s[a]
    s[a] = s[240 + x]
    s[240 + x] = tmp
    a = a + 1
}

function absorb_byte(b)
{
    absorb_nibble(b % 16)
    absorb_nibble(Math.floor(b / 16))
}

function output()
{
    update()
    return s[j]
}

function squeeze(out, outlen)
{
    shuffle()
    for (v = 0; v < outlen; v++) 
        out[v] = output()
}

function MD(txt){
  for (v = 0; v < 256; v++) 
      s[v] = v;
  a = i = j = 0
  w = 1
  for ( ii = 0; ii < txt.length; ii++ )
    absorb_byte(txt.charCodeAt(ii))
  squeeze(out, 32)
  return out
}
function h(x){
  return MD(x)
} 

var hash = h(document.getElementById("demo").innerHTML) 
document.getElementById("demo").innerHTML = "Hello JavaScript! hash = " + hash
</script> 

</body>
</html>
