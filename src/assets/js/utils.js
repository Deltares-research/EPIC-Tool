let server = process.env.VUE_APP_BACKEND_URL;

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
    let input = server + '/api/program/' + programId + '/question-' + questionType + '/?format=json';
    let response = await fetch(input, options);
    if (response.status !== 200) return [];
    return await response.json();
}

export async function loadProgress(programId, token) {
    const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        },
    }
    let answer = server + '/api/program/' + programId + '/progress/?format=json';
    let response = await fetch(answer, options);
    if (response.status !== 200) {
        return {};
    }
    const progress = await response.json();
    return progress.progress;
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
    let answer = server + '/api/question/' + questionId + '/answers/?format=json';
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
    let input = server + '/api/answer/' + answerId + '/';
    let res = await fetch(input, options);
    if (res.status != 200) {
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
    let input = server + '/api/answer/' + answerId + '/';
    await fetch(input, options);
}

export async function saveYesNoAnswer(answerId, justifyAnswer, shortAnswer, token) {
    const newAnswer = {};
    newAnswer.justify_answer = justifyAnswer;
    if (shortAnswer === 'Strongly disagree') {
        newAnswer.selected_choice = "STRONGLYDISAGREE"
    }
    if (shortAnswer === 'Disagree') {
        newAnswer.selected_choice = "DISAGREE"
    }
    if (shortAnswer === 'Neither agree nor disagree') {
        newAnswer.selected_choice = "NEITHERAGREENORDISAGREE"
    }
    if (shortAnswer === 'Agree') {
        newAnswer.selected_choice = "AGREE"
    }
    if (shortAnswer === 'Strongly agree') {
        newAnswer.selected_choice = "STRONGLYAGREE"
    }
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
    let input = server + '/api/answer/' + answerId + '/';
    await fetch(input, options);
}
