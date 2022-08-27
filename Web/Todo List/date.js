module.exports=getDate

function getDate() {
  var day = new Date();
  var options = {
    weekday: "long",
    day: "numeric",
    month: "long",
  };
  day = day.toLocaleString("en-US", options);
  return day;
}
