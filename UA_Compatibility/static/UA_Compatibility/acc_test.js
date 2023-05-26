var need_orientation_permission = false;
var tests_passed = false;

var generic_error = "An error occured.  This means that your phone is likely not compatible with the experiment.  Sorry for any disappointment"

function testAccPermission(e){

    try {
        console.log(e)
        if (e.acceleration.x === null)
        {
            throw "UndefinedInAccelerometerData"
        }
        else
        {
            jQuery('#passAll').show()
            tests_passed = true;
            window.removeEventListener("devicemotion", testAccPermission)
        }
    }
    catch (ex){
        jQuery("#needAccPermissionAndroid").show()
        window.removeEventListener("devicemotion", testAccPermission)
        tests_passed = true;
    }

    setTimeout(function(){
    jQuery('#testsRunning').hide()}, 1000);
}


function checkAccPermission(){
    window.addEventListener("devicemotion", testAccPermission)
    console.log("testing accelerometer permissions")
    setTimeout(function(){ window.removeEventListener("devicemotion", testAccPermission);
    if (!tests_passed){ jQuery('#failed').show()
        console.log("tests failed");
        }
    else {
        console.log("tests passed");
        }
    }, 1000)
    }


function getPermission(){

   if (need_orientation_permission){
     try {
          if (need_orientation_permission){
            DeviceOrientationEvent.requestPermission().then((response) => {
                try{
                  if (response === "granted") {
                    checkAccPermission()
                  }
                  else
                  {
                  }
                }
                catch (e) { alert(generic_error)}
                }).finally(() => {

                    checkAccPermission()

                });
              } else {
                try{
                    checkAccPermission()
                }catch (e){
                alert(generic_error)
                }
              }
       
      } catch (e) {
        /*alert(
          `Error encountered in request permission: ${e}`
        );*/
        alert(generic_error)
        }
    }
    else {
      // non iOS 13+
        console.log("no way of asking permissions - testing")
        checkAccPermission()
    }
}


jQuery(document).ready( function(){


  try {
    if (typeof DeviceOrientationEvent.requestPermission === 'function') {
      // iOS 13+
            if (typeof DeviceOrientationEvent.requestPermission === 'function') {
                need_orientation_permission = true;
                jQuery('#testAccelerometerAccessButton').on('click', function(){
                getPermission()

                })
                jQuery('#testAccelerometerAccessButton').show()
            }
            else
            {
                need_orientation_permission = false;
                checkAccPermission()
            }
        }
    else {
      // non iOS 13+
        console.log("no way of asking permissions - testing")
        checkAccPermission()
    }
     } catch (e) {

        need_orientation_permission = false;
        checkAccPermission()
   }

})
