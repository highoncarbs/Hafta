export const state = () => ({

    win: true

})

export const mutations = {
    TOGGLE_WIN(state) {
        state.win = !state.win
    },

}

export const getters = {
    get_win: state => {
        return state.win
    },

}
export const actions = {



}