
function xy()
    {   
        var x = document.cookie;
        
        if(x!="")
        {
            x = x.split(';');
            var js = x[0].split('=');
            var uname = x[1].split('=');
            console.log(x)

            if(js[1]==="1")
            {
                try{document.getElementById("100").style.display="none";}
                catch(err){console.log('remove')}
                try{document.getElementById("200").style.display="flex";}
                catch(err){console.log('remove')}
                try{document.getElementById("2000").style.display="flex";}
                catch(err){console.log('remove')}
                try{document.getElementById("20000").style.display="flex";}
                catch(err){console.log('remove')}

                console.log('remove')
            }
            
            
            else if(js[1]==="0")
            {
                    try{document.getElementById("100").style.display="flex";}
                    catch(err){console.log('remove')}
                    try{document.getElementById("200").style.display="none";}
                    catch(err){console.log('remove')}
                    try{document.getElementById("2000").style.display="none";}
                    catch(err){console.log('remove')}
                    try{document.getElementById("20000").style.display="none";}
                    catch(err){console.log('remove')}

                    console.log('remove')
            }
            

        }
        else
        {
            try{document.getElementById("200").style.display="none";}
            catch(err){console.log('remove')}
            try{document.getElementById("2000").style.display="none";}
            catch(err){console.log('remove')}
            try{document.getElementById("20000").style.display="none";}
            catch(err){console.log('remove')}
            try{document.getElementById("100").style.display="flex";}
            catch(err){console.log('remove')}
            console.log('remove')

        }
    }

