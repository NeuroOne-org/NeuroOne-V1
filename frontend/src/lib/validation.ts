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

/**
 * Patient intake.
 *
 * Mirrors `PatientCreate` in the API contract. The backend stores names in
 * two halves and takes a date of birth rather than an age, so the form asks
 * for exactly that instead of asking for something friendlier and guessing.
 */
export const patientIntakeSchema = z.object({
  first_name: z.string().min(1, "Enter the patient's first name").max(100),
  last_name: z.string().max(100).optional().or(z.literal("")),
  dob: z
    .string()
    .min(1, "Enter a date of birth")
    .refine((value) => {
      const date = new Date(value);
      return !Number.isNaN(date.getTime()) && date <= new Date();
    }, "Enter a date of birth in the past"),
  gender: z.enum(["male", "female", "other"], {
    required_error: "Select a gender",
  }),
  email: emailSchema,
  phone: z.string().min(1, "Enter a contact number").max(15),
  address: z.string().min(1, "Enter an address").max(500),
  blood_group: z.string().min(1, "Select a blood group"),
  allergies: z.string().max(500).optional().or(z.literal("")),
  emergency_contact: z.string().min(1, "Enter an emergency contact").max(255),
});
export type PatientIntakeInput = z.infer<typeof patientIntakeSchema>;

/** Mirrors `VisitCreate`. Vitals and symptoms are added after the visit exists. */
export const visitIntakeSchema = z.object({
  chief_complaint: z
    .string()
    .min(1, "Enter the presenting complaint")
    .max(255),
  history: z.string().max(5000).optional().or(z.literal("")),
  notes: z.string().max(5000).optional().or(z.literal("")),
});
export type VisitIntakeInput = z.infer<typeof visitIntakeSchema>;

export const BLOOD_GROUPS = [
  "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-",
] as const;
