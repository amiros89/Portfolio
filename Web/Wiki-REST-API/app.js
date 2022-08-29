const { urlencoded } = require("body-parser");
const bodyParser = require("body-parser");
const express = require("express");
const _ = require("lodash");
const app = express();
const mongoose = require("mongoose");
const port = 3000;
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

mongoose.connect("mongodb://localhost:27017/wikiDB");
const articlesSchema = {
  title: {
    type: String,
    required: true,
    unique: true,
  },
  content: {
    type: String,
    required: true,
  },
};

const Article = mongoose.model("Article", articlesSchema);

app
  .route("/articles")
  .get(function (req, res) {
    Article.find(function (err, articles) {
      if (!err) {
        res.send(articles);
      } else {
        console.log(err);
      }
    });
  })
  .post(function (req, res) {
    const articleTitle = req.body.title;
    const articleContent = req.body.content;
    const article = new Article({
      title: articleTitle,
      content: articleContent,
    });
    article.save();
    res.redirect("/articles/" + articleTitle);
  })
  .delete(function (req, res) {
    Article.deleteMany({}, function (err, deletedArticles) {
      if (!err) {
        res.send(deletedArticles);
      } else {
        console.log(err);
      }
    });
  });

app
  .route("/articles/:article")
  .get(function (req, res) {
    const articleTitle = req.params.article;
    Article.findOne({ title: articleTitle }, function (err, foundArticle) {
      if (!err) {
        if (foundArticle) {
          res.send(foundArticle);
        } else {
          res.send("Found no articles with title " + articleTitle);
        }
      } else {
        console.log(err);
      }
    });
  })
  .put(function (req, res) {
    const requestedArticle = req.params.article;
    const articleTitle = req.body.title;
    const articleContent = req.body.content;
    Article.findOne({ title: requestedArticle }, function (err, foundArticle) {
      if (!err) {
        if (foundArticle) {
          foundArticle.title = articleTitle;
          foundArticle.content = articleContent;
          foundArticle.save();
          res.redirect("/articles/" + articleTitle);
        } else {
          res.send("Found no articles with title " + requestedArticle);
        }
      } else {
        console.log(err);
      }
    });
  })
  .patch(function (req, res) {
    const requestedArticle = req.params.article;
    Article.updateOne(
      { title: requestedArticle },
      { $set: req.body},
      function (err) {
        if (!err) {
          res.send("Successfully updated article.");
        } else {
            res.send(err);
        }
      }
    );
  })
  .delete(function (req, res) {
    const requestedArticle = req.params.article;
    Article.findOneAndDelete(
      { title: requestedArticle },
      function (err, foundArticle) {
        if (!err) {
          if (foundArticle) {
            console.log(foundArticle);
            res.sendStatus(200);
          } else {
            res.sendStatus(404);
          }
        } else {
          console.log(err);
          res.sendStatus(500);
        }
      }
    );
  });

app.listen(port, function () {
  console.log("Server started successfully on port " + port);
});
