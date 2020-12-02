import React, { useEffect, useState } from "react";

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top,
  };
}
function print(e) {
  console.log(e);
}

function draw(el) {
  var ctx = el.getContext("2d");
  ctx.fillStyle = "#ffffff";

  ctx.lineWidth = 20;
  ctx.lineJoin = ctx.lineCap = "round";

  var isDrawing,
    points = [];

  el.onmousedown = function (e) {
    isDrawing = true;
    points.push(getMousePos(el, e));
  };

  el.onmousemove = function (e) {
    if (!isDrawing) return;

    ctx.fillRect(0, 0, el.width, el.height);
    points.push(getMousePos(el, e));

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (var i = 1; i < points.length; i++) {
      ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.stroke();
  };

  el.onmouseup = function () {
    isDrawing = false;
    points = [];
  };
}

export function Canvas() {
  const [_canvas, setCanvas] = useState(null);
  const [pred, setPred] = useState({
    Number: "",
    probability: "",
  });
  const url = "http://127.0.0.1:8000/api/recognize/";

  useEffect(() => {
    var el = document.getElementById("c");
    setCanvas(el);
    draw(el);
  }, []);

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const handleClick = async (e) => {
    const csrf_token = getCookie("csrftoken");
    const dataURL = _canvas.toDataURL();

    const data = await fetch(url, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrf_token,
      },

      body: JSON.stringify({
        data: dataURL,
      }),
    })
      .then(function (response) {
        return response.json();
      })
      .catch(function (err) {
        console.warn("Could not find the data");
      });
    if (!data) return;
    setPred(() => data);
    console.log(data);
    return data;
  };

  return (
    <>
      <canvas id="c" width={300} height={300}></canvas>
      <br />
      <button className="submit" onClick={handleClick}>
        Submit
      </button>
      <h1>{pred.Number}</h1>
      <h3>
        {pred.probability !== ""
          ? `With probability: ${pred.probability.toFixed(3)}`
          : "_____________________________"}
      </h3>
    </>
  );
}
