//Password match
var p_check = function() {
  if (document.getElementById('password').value ==
    document.getElementById('c_password').value) {
    document.getElementById('message').style.color = 'green';
    document.getElementById('message').innerHTML = 'Matching';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = 'Not Matching';
  }
}




