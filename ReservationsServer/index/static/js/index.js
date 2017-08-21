loadDateSelection()
//FIXME TODO work around all the window variables!!!
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    }
});

//FIXME begin loading the (quite big) svg file
$.getJSON("sitzverteilung", function(json) {
 window.seatReservationBackground = json
});


function loadDateSelection(){
    //FIXME cache finished html
    //FIXME TODO (animation) make sure that is contentDiv is in inital position
    //$('#contentDiv').addClass('moveIn')
    window.onresize = ()=>{
    }

    $('.flowButtons').addClass('hidden')

    if(!window.dateselection){
        //FIXME this is horrible #put in url via django templates?
        var newUrl = window.location.href+"dateselection"
        var request = $.ajax({
            method: "GET",
            url: newUrl,
            cache: true,
            //data: { date: date },
            success : function(text)
            {
                $('#contentDiv').html(text)
                $.getJSON("getdates", (dates)=>
                {
                    //FIXME move into createDateButtons method ALSO I am using the displayed date as a key for the actual date, which is ugly.
                    if (!window.selectedSeats){
                        window.toActualDates = []
                        window.selectedSeats = []
                        for (var i = 0; i < dates.length; i++) {
                            date = new Date(dates[i]).toLocaleDateString()
                            //FIXME
                            window.toActualDates[date] = dates[i]
                            window.selectedSeats[date] = []
                        }
                    }
                    var html = createDateButtons()
                    $("#dateField").html(html)
                    window.dateselection = $('#contentDiv').html()
                })
            }
        })
        request.fail(
            console.log(request)
            //ajaxFailedWarning(request, request.status)
        )
    }
    else {
        $('#contentDiv').html(window.dateselection)
    }
}


function createDateButtons() {
    if(jQuery.isEmptyObject(window.selectedSeats)){alert('There are currently no shows planned.')}
    var l = Object.keys(window.selectedSeats).length;
    //create the grid layout depending on how many buttons there are
    var rows = Math.ceil(l**0.5)
    var columns = Math.floor(l**0.5)
    $("#dateField").css({gridTemplateColumns : "repeat("+columns+", 1fr)"})
    $("#dateField").css({gridAutoRows : "repeat("+rows+", 1fr)"})

    var id = 0
    html = ""
    Object.keys(window.selectedSeats).forEach((date)=>{
        //FIXME inject within django???
        var buttonId = "buttonNr"+id

        html += "<button type = \"submit\""+
        "id=\""+buttonId+"\""+
        "onclick=\"onDateButtonClick(id)\""+
        "class = \"btn btn-primary dateButton\">"+
        date+
        "</button>"

        id++
    })
    return html
    //TODO
    //$("contentDiv").addClass('moveIn')
}



function onDateButtonClick(id){
    //$('#contentDiv').addClass('hideUp');

    var date = ($("#"+id).html())
    var newUrl = window.location.href+"sitzreservation"
    var request = $.ajax({
        method: "GET",
        url: newUrl,
        cache: true,
        success : function(text)
        {
            //FIXME this is horrible
            window.selectedDate = ($("#"+id).html())
            createSeatSelection(text)
        }
    })

    request.fail(
        //ajaxFailedWarning()
    );
}





function createSeatSelection(text){

    $('#contentDiv').html(text)

    $('.flowButtons').removeClass('hidden')

    $('#returnButton').click(loadDateSelection)

    $('#continueButton').click(createSummarizingText)

    draw()

    window.onresize = ()=>{
        setTimeout(draw, 10)
    }

}



function draw(){
    //Somehow this fixes the non-drawing issue.
    $('#svgColumn').parent().height()
    var svgCanvas = document.getElementById("svgCanvas")
    //FIXME use parents inner element width.
    var xSize = svgCanvas.width.baseVal.value
    var ySize = svgCanvas.height.baseVal.value

    if (xSize > ySize){
        ySize = (xSize/ySize)*ySize
        svgCanvas.height.baseVal.value = ySize
    }
    var json = window.seatReservationBackground
    $.get("getreservation/"+window.toActualDates[window.selectedDate], function(reservedSeat) {
    var reservedSeatList = JSON.parse(reservedSeat)
    var seatRadius = Math.min(
        ySize/(4.2*json.length**0.5),
        xSize/(3*json.length**0.5))

        for (var i = 0; i < json.length; i++){
            seat = json[i]

            var idString = seat.i
            var elm = svgCanvas.getElementById(idString)
            if(elm){elm.remove()}

            var newElement = document.createElementNS("http://www.w3.org/2000/svg", 'circle') //Create a path in SVG's namespace
            newElement.setAttribute("r", seatRadius)
            newElement.setAttribute("cx",seat.x*xSize)
            newElement.setAttribute("cy",seat.y*ySize)
            newElement.setAttribute("id", idString)
            //try to remove the element
            newElement.setAttribute("class", reservedSeatList.indexOf(seat.i) == -1 ? "free" : "reserved")
            var classes =  newElement.getAttribute("class")
            if(classes.indexOf("free") > -1 || classes.indexOf("selected") > -1 ){
                newElement.setAttribute("onclick", "clickOnSeat('"+idString+"')")
            } else {
                newElement.setAttribute("onclick", "alert('Bereits reserviert!')")
            }
            svgCanvas.appendChild(newElement)
            //if seat in window.selectedSeats make it selected on update
            //TODO Also make a function for selecting and deselecting a seat.
            var selectedSeats = window.selectedSeats[window.selectedDate]
            if(selectedSeats.indexOf(seat.i)>-1){
                if( classes.indexOf("free") > -1 ){
                    newElement.setAttribute("class", classes.replace("free","selected"))
                }
            }
        }
        //TODO
        //$('#contentDiv').toggleClass('moveIn')
        $('#dateInfo').html(window.selectedDate)
        });
}



    function clickOnSeat(seatName){
        //TODO save selected seats as cookie or after # in url.
        var element = document.getElementById(seatName)
        var classes = element.getAttribute("class")
        if( classes.indexOf("free") > -1 ){
            window.selectedSeats[window.selectedDate].push(seatName)
            element.setAttribute("class", classes.replace("free","selected"))
        }
        if( classes.indexOf("selected") > -1 ){
            window.selectedSeats[window.selectedDate].splice(window.selectedSeats[window.selectedDate].indexOf(seatName), 1)
            element.setAttribute("class", classes.replace("selected","free"))
        }
        //FIXME only do this when "Weiter" button is pressed.
        //createSummarizingText()
        $("#continueButton").attr('disabled', true)
        if(window.selectedSeats[window.selectedDate].length > 0){
            $("#continueButton").attr('disabled', false)
        }

    }



    function createSummarizingText (){
        var seats = JSON.parse(JSON.stringify(window.selectedSeats[window.selectedDate]))
        //remove everything but the number of the seat
        var numberOfSeats = seats.length
        seats = seats.map((seat)=>{return seat.replace ( /\D+/g, '' )})
        //sort by seat number
        seats = seats.sort(function(a, b){return parseInt(a)-parseInt(b)})
        var lastSeat = seats.pop()

        var html = []
        html[0] = "Sie sind im Begriff<b>"
        html[1] = "einen Sitz"
        html[2] = "</b>(nummer"
        html[3] = lastSeat+")"
        html[4] = "am <b>"+window.selectedDate+"</b>"

        if( window.selectedSeats[window.selectedDate].length > 1 ){
            //change what needs to be changed if plural is needed.
            html[1] = numberOfSeats+" Sitze"
            html[3] = seats.join(", ")+" und " + lastSeat+")";
        }

        html.push("zu reservieren.")

        $("#seatResume").html(html.join(" "))

    }







    function submitReservationRequest(){
    var request = $.post(window.location.href+"reserved",
        {
             date: window.toActualDates[window.selectedDate],
             seats: JSON.stringify(window.selectedSeats[window.selectedDate]),
             email: $("#emailField").val()
         },
        function(response)
            {
                //if email is valid and user not bot
                $('#contentDiv').html(response)
                $('#continueButton').addClass("hidden")
            })

        .fail(function(error) {
            console.log( error )
            if(error.status == 400){
                //keep modal open
                //FIXME
                window.setTimeout(()=>{$('#continueButton').click()}, 310)
                $('#emailErrorField').html("Bitte korrekte Email Adresse eingeben!")
            }
            if(error.status == 418){
                alert("Konnte Email nicht senden. Reservation nicht erfolgreich.")
            }
    })

    }


    function loadReservationConfirmationPrompt(){

    }





    //sets the seats for the current window.selectedDate
    function setSeats (seats) {
        //TODO FIXME
        Cookies.set('seats', JSON.stringify(seats[window.selectedDate]))
        }

    //gets the seats for the current window.selectedDate
    function getSeats () {
        var seats = Cookies.get('seats')
        if (seats == "undefined") {return undefined}
        return JSON.parse(seats[window.selectedDate])
        }

    //adds the seat for the current window.selectedDate
    function addSeat ( seat ) {
        if (getSeats() == undefined) {
        //     for (var i = 0; i < dates.length; i++) {
        //         date = new Date(dates[i]).toLocaleDateString()
        //         window.selectedSeats[date]=[]
        // }
        Cookies.set(getSeats().push(seat))
        }
    }

    //removes the seat for the current window.selectedDate
    function removeSeat ( name ) {
        setSeats(getSeats().splice(name, 1))
    }



    function ajaxFailedWarning(jqXHR, statusText){
        warning = ""
        warning += "Something went horribly wrong: \n"
        warning += jqXHR.status == 0 ? "You seem to be offline.\n" : ""
        warning += "\nstatus: "+jqXHR.status+" ("+jqXHR.statusText+")"
        alert(warning)
    }


    $("#myModal").keydown(
        (event)=>{
            if(event.keyCode == 13){
            submitReservationRequest()
            }
        }
    )
