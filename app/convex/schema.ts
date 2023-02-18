import { defineSchema, defineTable, s } from "convex/schema";

export default defineSchema({
  user: defineTable({
    email: s.string(),
    //user: s.id("users"),
    password: s.string(),
    learningStyle: s.string(),
  }),
  class: defineTable({
    name: s.string(),
    // tbd
  }),
});