import community from './community'
import core from './core'

const UniversalIntelligence = {
  core,
  community
}

export const Model = community.models.Model
export const Tool = community.tools.Tool
export const OtherTool = community.tools.Tool
export const Agent = community.agents.Agent
export const OtherAgent = community.agents.Agent

export default UniversalIntelligence