/**
 * Created by alasdairjohnson on 7/4/17.
 */
$(document).ready(function () {
  //table
    CreateTable1("users");
    // $("#AddClient").bind('click', function(){
    //     makeClientAddPop();
    // });
});



/**
 * Parama tableID: the id of the table we which to create
 * returns: creates a table with modals yay
 */
function CreateTable1(tableID) {//I know this is terible naming please forgive its 5 am
    var table = $("#" + tableID).DataTable({ //targets table and creates table
        "ajax": {
            "url": "/api/getUsers"
        },
        "columns": [
            {
                "data": "Name"
            }
        ]
    });
    $("#" + tableID + " tbody").on('click', 'tr', function() {
        console.log(window.location.href);
        CreateTable2("times", "1",table.row(this).data().id);//change this to update the other table
    });
    }

    function CreateTable2(tableID, user1, user2) {//I know this is terible naming please forgive its 5 am
    var table = $("#" + tableID).DataTable({ //targets table and creates table
        "ajax": {
            "url": "/api/getAvailability"+"/"+user1+"/"+user2
        },
        "columns": [
            {
                "data": "Time"
            }
        ]
    });
    }



function getModal(id) {
    console.log(id);
    $.get('/api/getClientsCheckedoutItems/' + id)
    .done(function(data) {
            $('#message-model-content').html(data["html"]);
            setDropDown(data["data"]);
            $('#user1Message').modal('show');
            $('#checkIn').on('click', function () {
            var checkbox = $(".itemCheckBox input:checkbox");
            sendData(checkbox, data["ClientID"]);
            $('#user1Message').modal('toggle');
            })
          });
}


function setDropDown(data){
    for (var key in data){
        setNumber(data[key]["CheckoutID"],data[key]["numCheckedOut"],data[key]["numCheckedOut"])
    }
}

function setNumber(classID, numberSelected, range){
    var $select = $("select." + classID);
    for (var i=1;i<=range;i++){
        $select.append($('<option></option>').val(i).html(i))
    }
    $select.val(numberSelected)
}

function processForm(checkbox, clientID) {
    var out = [];
    for (var index in checkbox){
        if (checkbox[index].checked){
            var data = {};
            data["checkedOutID"] = checkbox[index].id;
            data["numberReturn"] = $('select.' + checkbox[index].id).val();
            data["clientID"] = clientID;
            out.push(data);
        }
    }
    return JSON.stringify(out);
    }

function sendData(checkbox, clientID){
    $.ajax({
      type: "POST",
      url: "/api/returnItem",
      data: processForm(checkbox, clientID),
      success: function() {
                console.log("success");
            },
      dataType: "json",
      contentType: "json/application"
    });
}

/**
 * Created by alasdairjohnson on 11/11/17.
 */
