import axios from 'axios'

const state = {
  token: localStorage.getItem('access_token') || null,
  refreshToken: localStorage.getItem('refresh_token') || null,
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  isAuthenticated: false
}

const getters = {
  isAuthenticated: state => !!state.token && !!state.user,
  currentUser: state => state.user,
  userPermissions: state => state.user ? state.user.permissions : [],
  userRoles: state => state.user ? state.user.roles : [],
  hasPermission: (state) => (permission) => {
    return state.user && state.user.permissions && state.user.permissions.includes(permission)
  },
  hasRole: (state) => (role) => {
    return state.user && state.user.roles && state.user.roles.includes(role)
  }
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    state.isAuthenticated = !!token
    if (token) {
      localStorage.setItem('access_token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      localStorage.removeItem('access_token')
      delete axios.defaults.headers.common['Authorization']
    }
  },
  
  SET_REFRESH_TOKEN(state, refreshToken) {
    state.refreshToken = refreshToken
    if (refreshToken) {
      localStorage.setItem('refresh_token', refreshToken)
    } else {
      localStorage.removeItem('refresh_token')
    }
  },
  
  SET_USER(state, user) {
    state.user = user
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    } else {
      localStorage.removeItem('user')
    }
  },
  
  CLEAR_AUTH(state) {
    state.token = null
    state.refreshToken = null
    state.user = null
    state.isAuthenticated = false
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']
  }
}

const actions = {
  login({ commit }, { token, refreshToken, user }) {
    commit('SET_TOKEN', token)
    commit('SET_REFRESH_TOKEN', refreshToken)
    commit('SET_USER', user)
  },
  
  logout({ commit }) {
    commit('CLEAR_AUTH')
  },
  
  async refreshToken({ commit, state }) {
    try {
      if (!state.refreshToken) {
        throw new Error('No refresh token available')
      }
      
      const response = await axios.post('/api/auth/refresh', {}, {
        headers: {
          'Authorization': `Bearer ${state.refreshToken}`
        }
      })
      
      const newToken = response.data.access_token
      commit('SET_TOKEN', newToken)
      
      return newToken
    } catch (error) {
      commit('CLEAR_AUTH')
      throw error
    }
  },
  
  async fetchUserProfile({ commit, state }) {
    try {
      if (!state.token) {
        throw new Error('No token available')
      }
      
      const response = await axios.get('/api/auth/profile')
      commit('SET_USER', response.data.user)
      
      return response.data.user
    } catch (error) {
      commit('CLEAR_AUTH')
      throw error
    }
  },
  
  async initializeAuth({ commit, dispatch }) {
    const token = localStorage.getItem('access_token')
    const refreshToken = localStorage.getItem('refresh_token')
    const user = JSON.parse(localStorage.getItem('user') || 'null')
    
    if (token && refreshToken && user) {
      commit('SET_TOKEN', token)
      commit('SET_REFRESH_TOKEN', refreshToken)
      commit('SET_USER', user)
      
      try {
        // 驗證 token 是否仍然有效
        await dispatch('fetchUserProfile')
      } catch (error) {
        try {
          // 如果獲取用戶資料失敗，嘗試刷新 token
          await dispatch('refreshToken')
        } catch (refreshError) {
          // 如果刷新也失敗，清除認證狀態
          commit('CLEAR_AUTH')
        }
      }
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}