/* global Knowi */

import React, { useEffect } from 'react';

const KnowiChart = () => {

  useEffect(() => {
    const script = document.createElement('script');

    script.src = "https://www.knowi.com/minify/knowi-api.min.js";
    script.async = true;

    document.body.appendChild(script);

    script.onload = () => {
      Knowi.render('#knowi-div', {
        type: 'share',
        dashboard: 'WyobiiGcrraiigipLL7EwYsxAYs5tOBlmtgGeplYnoQ8iswie',
        view: {
          title: true,
          border: true,
          header: true,
          backgroundColor: "lightblue",
          setting: true
        }
      }, function () {
      });
    }

    return () => {
      document.body.removeChild(script);
    }
  }, []);

  const knowiStyle = {
    height: '500px'
  };

  return (
    <div id="knowi-div"i style={knowiStyle}></div>
  )
}

export default KnowiChart;

