$(function() {
    
    // initializes game score 

    let score = 0
    
    // starts game, renders a new board

    $('#start').on('click', function() {
        window.location='http://127.0.0.1:5000/board'
    })

    // handles the submitted guess

    $('form').on('submit', function(e) {
        e.preventDefault();
        handleGuess($('#guess').val())
    })

    //  accepts a string guess, and makes a request to the server which checks if guess word is valid 

    async function handleGuess(guess){
        if (guess) {
            try{
                const response = await axios({
                   url: `http://127.0.0.1:5000/check/${guess}`,
                   method: "POST" 
                });

                // display result to user

                $('#valid').text(response.data.result)

                // keep score, increases by length of guess word if guess was successful

                if (response.data.result === 'ok') {
                    score = score + guess.length;
                    $('#score').text(score);
                }
            } 
            catch(e) {
                console.log(e.message)
            }
        }
    }



})

