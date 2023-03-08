$(function() {
    
    // initializes game score 

    let score = 0

    // starts game, renders a new board

    $('#start').on('click', function() {
        window.location='http://127.0.0.1:5000/board'
    })

    // starts and displays a 60 second timer when a new game is started, when time is up it disables further guesses and alerts user

    function timer() {
        let n = 60;
        const i = setInterval(function() {
            n--
            $('#timer').text(n)
            if (n === 0) {
                $('#submit').prop('disabled', true) 
                setTimeout(()=>{
                    clearInterval(i)
                    alert('Time is up')},100)
                    updateScores();        
            }
        },1000)
    }

    // listen for board to load, at which point, call timer

    if(window.location.pathname === '/board') timer();

    // handles the submitted guess

    $('form').on('submit', function(e) {
        e.preventDefault();
        handleGuess($('#guess').val())

    })

    // sends a request to server with new score

    async function updateScores() {
        try {
            const response = await axios({
                url: `http://127.0.0.1:5000/update`,
                method: "POST",
                data: {'score': score} 
            })
            $('#totalGames').text(response.data.gamesPlayed)
        }
        catch (e) {
            console.log(e.message)
        }
    }

    //  accepts a string guess, and makes a request to the server which checks if guess word is valid 

    async function handleGuess(guess){
        if (guess) {
            try{
                const response = await axios({
                   url: `http://127.0.0.1:5000/check`,
                   method: "POST", 
                   data: {'guess': guess}
                });

                // display result to user

                $('#valid').text(response.data.result)

                // keep score, increases by length of guess word if guess was successful

                if (response.data.result === 'ok') {
                    score = score + guess.length;
                    $('#score').text(score);
                }

                $('#guess').val('')
            } 
            catch(e) {
                console.log(e.message)
            }
        }
    }
})

