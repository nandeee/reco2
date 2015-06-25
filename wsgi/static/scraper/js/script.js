$(function() {
    var interval = 1000;
    console.log("I'm ready!");
    $("#getLinks").click(function() {
        $("paper-spinner").attr("active", "");
        console.log("Initiated.");
        $.ajax({
            url: "/scraper/getLinks/" + $("select#city").val() + "/" + $("select#category").val()
        }).done(function(data) {
            document.querySelector('#toast2').show();
            console.log(data);
            $("#total").text(data["retTot"]);
            console.log(window.location.origin + "/static/txt/" + data["fileName"]);
            $("paper-spinner").removeAttr("active");
            $("#processFile").removeAttr("disabled");
        });
    });
    $("#genExcel").click(function() {
        console.log("Initiated.");
        $.ajax({
            url: "/scraper/genExcel/" + $("select#city").val() + "/" + $("select#category").val()
        }).done(function(data) {
            console.log(data);
            console.log(window.location.origin + "/static/txt/" + data["fileName"]);
            $("a").attr("href", window.location.origin + "/static/txt/" + data["fileName"])
            $("a").removeClass("hide")
        });
    });
    $("paper-fab.blue").click(function() {
        console.log("Downloading...");
    });
    $("#delAll").click(function() {
        console.log("Initiated.");
        $.ajax({
            url: "/scraper/delAll/"
        }).done(function(data) {
            console.log(data);
        });
    });
    $("#processFile").click(function() {
        setTimeout(doAjax, interval);
        console.log("Initiated.");
        $.ajax({
            url: "/scraper/processFile/" + $("select#city").val() + "/" + $("select#category").val()
        }).done(function(data) {
            console.log(data);
            console.log(window.location.origin + "/static/txt/" + data["fileName"]);
        });
    });

    function doAjax() {
        $.ajax({
            url: "/scraper/getPos/" + $("select#city").val() + "/" + $("select#category").val(),
            success: function(data) {
                // console.log(data);
                $("#current").text(data["pos"]);
                $("#errors").text(data["retErr"]);
                if ($("#current").text() == $("#total").text()) {
                    document.querySelector('#toast3').show();
                    console.log("It's done!");
                    $("#genExcel").removeAttr("disabled");
                    return;
                }
                setTimeout(doAjax, interval);
            },
            error: function(xhr, status, error) {
                console.log("Error!");
                console.log(xhr);
                console.log(status);
                console.log(error);
                console.log("Retrying...")
                $.ajax(this);
                return;
            }
        });
    }
});
