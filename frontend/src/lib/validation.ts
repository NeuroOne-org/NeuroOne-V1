import { z } from "zod";

const DISPOSABLE_DOMAINS = new Set([
  "mailinator.com",
  "tempmail.com",
  "guerrillamail.com",
  "10minutemail.com",
  "throwawaymail.com",
  "yopmail.com",
  "trashmail.com",
]);

const emailSchema = z
  .string()
  .email("Enter a valid email address")
  .refine((email) => !DISPOSABLE_DOMAINS.has(email.split("@")[1]?.toLowerCase()), {
    message: "Please use a permanent email address, not a disposable one",
  });

const usernameSchema = z
  .string()
  .min(3, "At least 3 characters")
  .max(50, "50 characters max")
  .regex(/^[a-zA-Z0-9_.]+$/, "Letters, numbers, dots, and underscores only");

const strongPasswordSchema = z
  .string()
  .min(8, "At least 8 characters")
  .regex(/[a-z]/, "Add a lowercase letter")
  .regex(/[A-Z]/, "Add an uppercase letter")
  .regex(/[0-9]/, "Add a number")
  .regex(/[^A-Za-z0-9]/, "Add a special character");

export const loginSchema = z.object({
  email: z.string().min(1, "Enter your username or email"),
  password: z.string().min(1, "Enter your password"),
});
export type LoginInput = z.infer<typeof loginSchema>;

export const signupSchema = z
  .object({
    full_name: z.string().min(2, "Enter your full name"),
    username: usernameSchema,
    email: emailSchema,
    role: z.enum(["doctor", "researcher"], {
      required_error: "Select a role",
    }),
    password: strongPasswordSchema,
    confirm_password: z.string(),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
  });
export type SignupInput = z.infer<typeof signupSchema>;

export const otpSchema = z.object({
  otp: z.string().length(6, "Enter the 6-digit code").regex(/^\d+$/, "Digits only"),
});
export type OtpInput = z.infer<typeof otpSchema>;

export const forgotPasswordSchema = z.object({
  email: z.string().email("Enter a valid email address"),
});
export type ForgotPasswordInput = z.infer<typeof forgotPasswordSchema>;

export const resetPasswordSchema = z
  .object({
    otp: z.string().length(6, "Enter the 6-digit code").regex(/^\d+$/, "Digits only"),
    new_password: strongPasswordSchema,
    confirm_new_password: z.string(),
  })
  .refine((data) => data.new_password === data.confirm_new_password, {
    message: "Passwords do not match",
    path: ["confirm_new_password"],
  });
export type ResetPasswordInput = z.infer<typeof resetPasswordSchema>;

export const patientIntakeSchema = z.object({
  full_name: z.string().min(2, "Enter the patient's full name"),
  age: z.coerce
    .number({ invalid_type_error: "Age is required" })
    .min(1, "Enter a valid age")
    .max(120, "Enter a valid age"),
  gender: z.enum(["male", "female", "other"], {
    required_error: "Select a gender",
  }),
  mmse_score: z.coerce
    .number()
    .min(0, "MMSE score ranges from 0–30")
    .max(30, "MMSE score ranges from 0–30")
    .optional()
    .or(z.literal("").transform(() => undefined)),
  family_history: z.boolean().default(false),
  notes: z.string().max(2000).optional(),
});
export type PatientIntakeInput = z.infer<typeof patientIntakeSchema>;
