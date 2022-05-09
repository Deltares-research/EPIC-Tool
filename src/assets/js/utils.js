export async function loadQuestions(programId, questionType, token) {
    const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        },
    }
    let input = 'http://localhost:8000/api/program/' + programId + '/question-' + questionType + '/?format=json';
    let response = await fetch(input, options);
    if (response.status !== 200) return [];
    return await response.json();
}

export async function loadAnswer(questionId, token) {
    const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        },
    }
    let answer = 'http://localhost:8000/api/question/' + questionId + '/answers/?format=json';
    let response = await fetch(answer, options);
    if (response.status !== 200) {
        return {};
    }
    return await response.json();
}
export async function saveSelectedChoiceAnswer(answerId, justifyAnswer, selectedAnswer, token) {
    const newAnswer = {};
    newAnswer.justify_answer = justifyAnswer;
    newAnswer.selected_choice = selectedAnswer;
    const options = {
        method: 'PATCH',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        },
        body: JSON.stringify(newAnswer),
    }
    let input = 'http://localhost:8000/api/answer/' + answerId + '/';
    let res = await fetch(input, options);
    if(res.status != 200){
        alert("Error when trying to save answer")
    }
}
export async function saveSelectedProgramsAnswer(answerId, selectedPrograms, token) {
    const newAnswer = {};
    newAnswer.justify_answer = "";
    newAnswer.selected_programs = selectedPrograms;
    const options = {
        method: 'PATCH',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        },
        body: JSON.stringify(newAnswer),
    }
    let input = 'http://localhost:8000/api/answer/' + answerId + '/';
    await fetch(input, options);
}

export async function saveYesNoAnswer(answerId, justifyAnswer, shortAnswer, token) {
    const newAnswer = {};
    newAnswer.justify_answer = justifyAnswer;
    newAnswer.short_answer = shortAnswer;
    const options = {
        method: 'PATCH',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        },
        body: JSON.stringify(newAnswer),
    }
    let input = 'http://localhost:8000/api/answer/' + answerId + '/';
    await fetch(input, options);
}
