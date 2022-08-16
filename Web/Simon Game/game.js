var buttonColors = ["red", "blue", "green", "yellow"];
var gamePattern = [];
var userClickedPattern = [];
var level = 0;
var gameStarted = false;

function nextSequence() {
  userClickedPattern = [];
  var randomNumber = Math.floor(Math.random() * 4);
  var randomChosenColour = buttonColors[randomNumber];
  var level = gamePattern.length;
  gamePattern.push(randomChosenColour);
  playSound(randomChosenColour);
  $("#" + gamePattern[gamePattern.length - 1]).keypress();
  $("h1").text("Level " + level);
}

function playSound(name) {
  // Bind keypress buttons to be able to play button sound regardless of user activity 
  $("#" + name).keypress(function () {
    var sound = new Audio("sounds/" + name + ".mp3");
    sound.play();
  });
  // Sound per user click
  $("#" + name).click(function () {
    var sound = new Audio("sounds/" + name + ".mp3");
    sound.play();
  });
}

function checkAnswer(currentLevel) {
  if (userClickedPattern[currentLevel] != gamePattern[currentLevel]) {
    console.log("wrong");
    gameOver();
  } else {
    console.log("right");
    if (userClickedPattern.length === gamePattern.length) {
      console.log("success");
      setTimeout(nextSequence, 1000);
    }
  }
}

function gameOver() {
  var audio = new Audio((src = "sounds/wrong.mp3"));
  audio.play();
  $("body").addClass("game-over");
  setTimeout(function () {
    $("body").removeClass("game-over");
  }, 200);
  $("h1").text("Game Over, Press Any Key to Restart");
  startOver();
}

function startOver() {
  level = 0;
  gameStarted = false;
  gamePattern = [];
}

// Event Listeners

$(".btn").keypress(function (event) {
  var color = event.target.id;
  playSound(color);
  $("#" + color)
    .fadeOut(500)
    .fadeIn(500);
});

$(".btn").click(function (event) {
  var userChosenColour = event.target.id;
  userClickedPattern.push(userChosenColour);
  playSound(userChosenColour);
  console.log(userChosenColour);
  $("#" + userChosenColour)
    .fadeOut(500)
    .fadeIn(500);
  checkAnswer(userClickedPattern.length - 1);
});

$(document).keypress(function () {
  if (gameStarted === false) {
    $("h1").text("Level " + level);
    gameStarted = true;
    nextSequence();
  }
});


