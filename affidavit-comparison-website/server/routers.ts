import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, router } from "./_core/trpc";
import { getAllAffidavitData, getComments, addComment, deleteComment } from "./db";
import { z } from "zod";

export const appRouter = router({
    // if you need to use socket.io, read and register route in server/_core/index.ts, all api should start with '/api/' so that the gateway can route correctly
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  affidavit: router({
    getData: publicProcedure.query(async () => {
      const data = await getAllAffidavitData();
      return data;
    }),
  }),

  comments: router({
    getAll: publicProcedure
      .input(z.object({
        sectionNumber: z.string().optional(),
        paragraphNumber: z.string().optional(),
        paragraphType: z.enum(["AD", "JR", "DR"]).optional(),
      }))
      .query(async ({ input }) => {
        const comments = await getComments(input);
        return comments;
      }),
    
    add: publicProcedure
      .input(z.object({
        sectionNumber: z.string(),
        paragraphNumber: z.string(),
        paragraphType: z.enum(["AD", "JR", "DR"]),
        content: z.string().min(1),
        author: z.string().optional(),
      }))
      .mutation(async ({ input }) => {
        const comment = await addComment(input);
        return comment;
      }),
    
    delete: publicProcedure
      .input(z.object({
        id: z.number(),
      }))
      .mutation(async ({ input }) => {
        await deleteComment(input.id);
        return { success: true };
      }),
  }),
});

export type AppRouter = typeof appRouter;
