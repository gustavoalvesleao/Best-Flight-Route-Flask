// Query route

const apiUrl = "http://localhost:5001/";

(function () {
  $(".form-query-route").on("submit", function (event) {
    event.preventDefault();
    $(".alert").hide();
    $(".result-titles").hide();
    this.classList.add("was-validated");
    if (this.checkValidity() === false) {
      const startValidity = event.target[1].validity.valid;
      const endValidity = event.target[2].validity.valid;
      if (startValidity === false || endValidity === false) {
        $(".alert-route-query").show();
      }
    } else {
      handleQueryForm(this);
    }
  });
})();

function handleQueryForm(form) {
  const formData = $(form).serializeArray();
  $.ajax({
    type: "GET",
    url: `${apiUrl}getRoute?start=${formData[0].value}&end=${formData[1].value}`,
    headers: {
      "Content-Type": "application/json",
    },
    beforeSend: function beforeSend() {
      $(".form-query-route").removeClass("was-validated");
    },
    success: function success(xhr) {
      $(".result-query-title").show();
      $("#result-query").text(xhr.result);
    },
    error: function error(xhr) {
      $(".result-query-title").show();
      $("#result-query").text(xhr.responseJSON.result);
    },
  });
}

// Add route
(function () {
  $(".form-add-route").on("submit", function (event) {
    event.preventDefault();
    $(".alert").hide();
    $(".result-titles").hide();
    this.classList.add("was-validated");
    if (this.checkValidity() === false) {
      const startValidity = event.target[1].validity.valid;
      const endValidity = event.target[2].validity.valid;
      const costValidity = event.target[3].validity.valid;
      if (
        startValidity === false ||
        endValidity === false ||
        costValidity === false
      ) {
        $(".alert-route-add").show();
      }
    } else {
      handleAddForm(this);
    }
  });
})();

function handleAddForm(form) {
  const formData = $(form).serializeArray();
  const payload = {
    start: formData[0].value,
    end: formData[1].value,
    cost: formData[2].value,
  };
  $.ajax({
    type: "POST",
    url: `${apiUrl}addRoute`,
    headers: {
      "Content-Type": "application/json",
    },
    data: JSON.stringify(payload),
    beforeSend: function beforeSend() {
      $(".form-add-route ").removeClass("was-validated");
    },
    success: function success() {
      $(".alert-success").show();
    },
    error: function error() {
      $(".alert-route-add").show();
    },
  });
}
