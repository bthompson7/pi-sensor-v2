function getTempData() {

  document.getElementById("temp-sensor-1").innerHTML = "Loading Data...";
  document.getElementById("temp-sensor-2").innerHTML = "Loading Data...";
  //1st temp sensor
  var http = new XMLHttpRequest();
  http.onreadystatechange = function () {

    if (this.readyState == 4 && this.status == 200) {
      var tempData1 = JSON.parse(http.response);
      var tempValue = tempData1['temp'];
      var humidValue = tempData1['humid'];
      var normalDate = tempData1['last_updated_normal'];
      var unixTime = tempData1['last_updated'];

      var sensorInfoElement = document.getElementsByClassName("sensor-info-1")[0];


      //display the data
      var stringToDisplay = "Temperature: " + tempValue + "&#176;F   " + " Humidity: " + humidValue + "%";
      document.getElementById("temp-sensor-1").innerHTML = stringToDisplay;
      document.getElementById("hidden-time-1").innerHTML = unixTime;

      document.getElementById("last-updated-1").innerHTML = "Last Updated: " + timeSince(unixTime);
    } else if (this.readyState == 4 && this.status != 200) {

      console.error(http.response);
      document.getElementById("temp-sensor-1").innerHTML = http.response;
    }
  };

  http.open("GET", "/getTemp1");
  http.send();

  //2nd temp sensor
  var http2 = new XMLHttpRequest();
  http2.onreadystatechange = function () {

    if (this.readyState == 4 && this.status == 200) {
      var tempData2 = JSON.parse(http2.response)
      var tempValue = tempData2['temp'];
      var humidValue = tempData2['humid'];
      var normalDate = tempData2['last_updated_normal'];
      var unixTime = tempData2['last_updated'];
      var sensorInfoElement = document.getElementsByClassName("sensor-info-2")[0];

      //display the data
      var stringToDisplay = "Temperature: " + tempValue + "&#176;F   " + " Humidity: " + humidValue + "%";
      document.getElementById("temp-sensor-2").innerHTML = stringToDisplay;
      document.getElementById("last-updated-2").innerHTML = "Last Updated: " + timeSince(unixTime);
      document.getElementById("hidden-time-2").innerHTML = unixTime;


    } else if (this.readyState == 4 && this.status != 200) {
      console.error(http2.response);
      document.getElementById("temp-sensor-2").innerHTML = http2.response;
    }
  };

  http2.open("GET", "/getTemp2");
  http2.send();
}

function renderTimeSince(unixTime) {
  var sensorTime1 = document.getElementById("hidden-time-1").innerHTML;
  var sensorTime2 = document.getElementById("hidden-time-2").innerHTML;
  document.getElementById("last-updated-1").innerHTML = "Last Updated: " + timeSince(sensorTime1);
  document.getElementById("last-updated-2").innerHTML = "Last Updated: " + timeSince(sensorTime2);
}

// Please ignore this disaster
function timeSince(date) {

  var seconds = Math.floor((new Date() - date) / 1000);
  var intervalType;

  var interval = Math.floor(seconds / 31536000);
  if (interval >= 1) {
    intervalType = 'year';
  } else {
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) {
      intervalType = 'month';
    } else {
      interval = Math.floor(seconds / 86400);
      if (interval >= 1) {
        intervalType = 'day';
      } else {
        interval = Math.floor(seconds / 3600);
        if (interval >= 1) {
          intervalType = "hour";
        } else {
          interval = Math.floor(seconds / 60);
          if (interval >= 1) {
            intervalType = "minute";
          } else {
            interval = seconds;
            intervalType = "second";
          }
        }
      }
    }
  }

  if (interval > 1 || interval === 0) {
    intervalType += 's ago';
  }

  return interval + ' ' + intervalType;
}


getTempData();


setInterval(getTempData, 300000); //300000
setInterval(renderTimeSince, 1000);


